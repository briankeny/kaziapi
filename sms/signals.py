from django.dispatch import receiver,Signal
from .talk import SMS
from jobs.models import JobPost,JobApplication

send_job_enquiries_to_client = Signal()
@receiver(send_job_enquiries_to_client)
def send_available_jobs(sender, instance, recepient,*args, **kwargs):
    try:
        jobs = JobPost.objects.filter(title__in=instance.industry)
        data = list(jobs.values())
        jobs = data[:5]

        message = f"Hi {instance.full_name},"
        
        if len(jobs) > 0:
            message+=f"\n We found {len(jobs)} jobs that you can apply."
            for j in jobs:
                pid = j['post_id']
                title = j['title']
                message += f"\n {pid} {title}"

        else:
            message+= "We could not find any job matching your profile at the moment"

        message+='\n Thank You!'
        sms = SMS(recipients=[recepient],message=message)
        sms.send()
    except Exception as e:
        print(str(e))
        pass


send_job_applications_to_client = Signal()
@receiver(send_job_applications_to_client)
def send_application_sms(sender, instance, recepient,*args, **kwargs):
    try:
        # Get all applications
        aps = JobApplication.objects.filter(applicant=instance.user_id)

        # Send only ten according to latest
        jobs = aps[:10]
        
        message = f"""Hi {instance.full_name}
        We found {len(aps)} jobs that you applied """
        if len(jobs) > 0:    
            for j in jobs:
                message += f"\n Title:{j.jobpost.title}  Status {j.status}"
    
        sms = SMS(recipients=[recepient],message=message)
        sms.send()
    except Exception as e:
        print(str(e))
        pass
