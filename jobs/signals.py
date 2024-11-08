import json
import random
import re
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User,UserSkill,UserInfo
from jobs.models import JobPost,JobApplication,Job,UserJobPostInteraction
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
                'description' :job_desc[:100],
                'employment_type' :jobpost.employment_type,
                'experience_level' :jobpost.experience_level,
                'location':jobpost.location
            }

            # Get the required job skills  
            category = jobpost.category

            jobskills=[]
            if category :
                job = Job.objects.filter(job_id=category.job_id).values('job_skills')
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
            prompt = "Intructions: Award a score to a blue collar job seeker between 1 to 100 depending on their profile. Compare the applicant skills,bio, profession with the job profile"
            prompt +=f"\n userdetails: {personal_info} , userskills: {userskills} other user info  {additional_user_data}"
            prompt +=f"\n jobdetails: {job_info} , requiredjobskills: {jobskills}"
            prompt +="\n Respond with format, a python dictionary object for easy formating   { 'score': 'userscore' , 'reason' : 'Give a brief reason' } "

            ai_class = AI(prompt=prompt)
            ai_resp = ai_class.generateAIresponse() 
            
            def extract_json(response_string):
                # Use regex to find the JSON object within triple backticks
                match = re.search(r'```json\s*({.*?})\s*```', response_string, re.DOTALL)
                if match:
                    json_str = match.group(1)  # Extract JSON content
                    try:
                        # Convert the JSON string into a dictionary
                        json_data = json.loads(json_str)
                        return json_data
                    except json.JSONDecodeError:
                        score = random.choice([0,5,15,30])
                        return {'score' :score ,'reason':'Reason not provided'}
                else:
                    score = random.randint(5,40)
                    return {'score' :score, 'reason':'Reason not provided'}
             
            json_data = extract_json(ai_resp)
            
            # print(f'AI RESPONDED WITH {ai_resp}')
            if (ai_resp):
                application = JobApplication.objects.get(jobpost=instance.jobpost.post_id,applicant=user.user_id)
                score = json_data.get('score',8)
                reason = json_data.get('reason','')
                application.score = score
                application.comments = reason
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
                 sms = SMS(recipients=[mobile_num],message=message)
                 sms.send()

    except Exception as e:
        print(f'Error concluding job applications: {str(e)}')
        pass