from django.dispatch import receiver,Signal
from .talk import SMS
from jobs.models import JobPost,JobApplication,Job

send_job_enquiries_to_client = Signal()
@receiver(send_job_enquiries_to_client)
def send_available_jobs(sender, instance, recepient,*args, **kwargs):
    try:
         # Get the user profession or industry
        profession = instance.industry or 'empty'

        # Find the category id for this profession
        categories = Job.objects.filter(job_name__icontains = profession).values('job_id')
        jobs = []

        # Construct the message to send to client
        message = f"Hi {instance.full_name},"

        if categories.count() > 0:
            ids = [item["job_id"] for item in list(categories)]
            j_posts = JobPost.objects.filter(category__in=ids) 
            data = list(j_posts.values('post_id','title'))
            # First five jobs
            jobs = data[:5]
            if len(jobs) > 0:
                message+=f"\n We found {len(jobs)} jobs that you can apply."
                for j in jobs:
                    pid = j['post_id']
                    title = j['title']
                    message += f"\n {pid} {title}"
                message += 'Reply with #APPLY to apply for the job'
        else:
            message+= "\n We could not find any job matching your profile at the moment"
    
        message+='\n Thank You!'
        sms = SMS(recipients=[recepient],message=message)
        sms.send()
    except Exception as e:
        pass


send_job_applications_to_client = Signal()
@receiver(send_job_applications_to_client)
def send_application_sms(sender, instance, recepient,*args, **kwargs):
    try:
        # Get all applications
        aps = JobApplication.objects.filter(applicant=instance.user_id)

        # Send only ten according to latest
        jobs = aps[:5]
        
        message = f"""Hi {instance.full_name}
        We found {len(aps)} jobs that you applied """
        if len(jobs) > 0:    
            for j in jobs:
                message += f"\n Id {j.jobpost.post_id} Title:{j.jobpost.title}  Status:{j.status},"

        message+= "\n Thank You! Regards @KaziMtaani"
        sms = SMS(recipients=[recepient],message=message)
        sms.send()
    except Exception as e:
        pass
