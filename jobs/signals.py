import re
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from users.models import User,UserSkill,UserInfo
from jobs.models import JobPost,JobApplication,Job
from django.dispatch import receiver
from kaziai.ai import AI


# If a job application has been posted calculate the score for the applicant  
@receiver(post_save, sender=JobApplication)
def update_applicant_score(sender,instance,created,**kwargs):
    if created:
        try:
            job = instance.jobpost
            application = JobApplication.objects.get(jobpost=job)
            applicant = instance.applicant
            jobskills=[]
            userskills =[]

            # Get the jobpost details 
            jobpost = JobPost.objects.get(post_id=job)
            
            job_info = {
                'title' : jobpost.title,
                'description' :jobpost.description,
                'employment_type' :jobpost.employment_type,
                'experience_level' :jobpost.experience_level,
                'location':jobpost.location
            }

            # Get the required job skills  
            category = jobpost.category

            if category :
                job = Job.objects.filter(job_id=jobpost.category)
                jobskills = list(job.values('job_skilss'))


            # Get Applicant profile
            user = User.objects.get(user_id = applicant)
            
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
            Between 1 to 100 give a score for this blue collar job seeker based on the provided profile

            user = {personal_info}
            userskills = {userskills}
            other  details = {additional_user_data}

            Job Profile Being Applied and required skills 
            job = {job_info}
            jobskills = {jobskills}

            return response in this manner since the response is an input to another python program. No extra words my
            program will look for startscore and endscore then split the two and take the score  
            
            reason = "#Give reason in a string in under 100 characters"

            candidate_score = "startscore  (#Give a score value between 0-100 )  endscore"
            
            """

            ai_class = AI(prompt=prompt)
            ai_resp = ai_class.generateAIresponse() 

            def  format_airesp_find_score(text=''):
                score =0
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

            if (ai_resp):
                score = format_airesp_find_score(str(ai_resp))
                application.score = score
                application.save()

        except Exception as e:
            print('Found Error')
            pass
