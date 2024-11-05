import re
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User,UserSkill,UserInfo
from jobs.models import JobPost,JobApplication,Job
from django.dispatch import receiver,Signal
from kaziai.ai import AI
from notifications.signals import save_Notification
from sms.talk import SMS

# If a job application has been posted calculate the score for the applicant  
@receiver(post_save, sender=JobApplication)
def update_applicant_score(sender,instance,created,**kwargs):
    if created:
        try:
            jobpost = instance.jobpost
            applicant = instance.applicant
            jobskills=[]
            userskills =[]

            job_desc = jobpost.description
            
            job_info = {
                'title' : jobpost.title,
                'description' :job_desc[:150],
                'employment_type' :jobpost.employment_type,
                'experience_level' :jobpost.experience_level,
                'location':jobpost.location
            }

            # Get the required job skills  
            category = jobpost.category.job_id

            jobskills=[]
            if category :
                job = Job.objects.filter(job_id=category).values('job_skills')
                jobskills.extend(list(job))

            # Get Applicant profile
            user = User.objects.get(user_id = applicant.user_id)
            
            personal_info = {
                'fullname': user.full_name,
                 'profession':user.industry,
                 'bio': user.bio ,
                 'location' : user.location
            }
            
            # Get applicant additional info
            userinfo = UserInfo.objects.filter(user=user.user_id)
            additional_user_data = list(userinfo.values_list( 'subject','title','description','start_date' ,'end_date'))

            # Get user skills
            userskills = UserSkill.objects.filter(user=user.user_id)
            userskills = list(userskills.values('skill_name'))

            #Create text prompt to gemini to calculate the score 
            prompt = f"""
            Between 1 to 100 give a score for this blue collar job seeker based on the given profile. Be Very strict
            user = {personal_info}
            userskills = {userskills}
            other  details = {additional_user_data}
            Job Profile Being Applied and required skills 
            job = {job_info}
            jobskills = {jobskills}

            Return response in this manner since the response is an input to another python program. No extra words my
            program will look for startscore and endscore then split the two and take the score. Also provide a reason in under  100 words

            candidate_score = "startscore  (#Give a score value between 0-100 )  endscore"           
            reason = "#Give reason in a string in under 100 characters"
            """

            ai_class = AI(prompt=prompt)
            ai_resp = ai_class.generateAIresponse() 

            def  format_airesp_find_score(text=''):
                score = 10
                try:
                    # Extract the score using regex to handle whitespace and format
                    # Search for the score in the format of 'startscore <score> endscore'
                    match = re.search(r'startscore\s+(\d+)\s+endscore', text)
                    if match:
                        score = int(match.group(1))  # Convert the captured score to an integer
                        return score  # Output: 23
                    else:
                        return 5
                except Exception as e:
                    return score
            
            print(f'AI RESPONDED WITH {ai_resp}')
                

            if (ai_resp):
                application = JobApplication.objects.get(jobpost=instance.jobpost.post_id,applicant=user.user_id)
                score = format_airesp_find_score(str(ai_resp))
                application.score = score
                application.status = 'reviewed'
                application.save()

        except Exception as e:
            print('Found Error',e)
            pass


close_job_post_applications = Signal()
@receiver(close_job_post_applications)
def conclude_job_application(sender, instance, *args, **kwargs):
    try:
        post = instance
        applications = JobApplication.objects.filter(jobpost=post.post_id)
        subject = f"Job Update by {post.recruiter.full_name}"
        choices = ['accepted', 'declined']

        for item in applications:
            application_status = item.status
            if application_status not in choices:
                application_status = 'declined'
                item.status = application_status
                item.save()

            message = (
                f"Hi, {item.applicant.full_name},\nThe hiring process for the '{post.title}' job has been concluded. "
                f"Your application has been {application_status}. Thank you for participating in this process. "
                f"Contact your employer {post.recruiter.full_name} for more details."
            )
            save_Notification(subject, message,'jobpost',item.applicant, f'{post.post_id}')

            if item.applicant.mobile_verified:
                 mobile_num = str(item.applicant.mobile_number)
                 print(f'Found mobile {mobile_num}')
                 sms = SMS(recipients=[mobile_num],message=message)
                 sms.send()

    except Exception as e:
        print(f'Error concluding job applications: {str(e)}')