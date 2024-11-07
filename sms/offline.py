from users.models import User 
from jobs.models import JobApplication,JobPost

class Offline:
    def __init__(self,mobile_number, text):
        self.mobile_number = mobile_number
        self.text = text
        self.post_id = None
    
    def  actionCenter(self):
        user = None
        try:
            user = User.objects.get(mobile_number=self.mobile_number)
        except User.DoesNotExist:
            return self.rejectMessage
        
        if user is None:
            return self.rejectMessage
        
     
        if '#apply' in self.text.lower():
            clean_list = self.text.lower().replace('\n','').split('#apply')
            id = None
            for i in  clean_list:
                try:
                    inp = int(i)
                    id = inp
                except Exception as e:
                        pass
            if id is None:
                return f'Hey {user.full_name} to apply any job please start with #APPLY followed by job id like. #APPLY 23'
            resp = self.applyJob(id,user)
            return resp
        
        elif  '#reject' in self.text.lower():
            clean_list = self.text.lower().replace('\n','').split('#reject')
            id = None
            for i in  clean_list:
                try:
                    inp = int(i)
                    id = inp
                except Exception as e:
                        pass
            if id is None:
                return f"""
                Hey {user.full_name},
                To reject any job your application start with the word #REJECT followed by the job id 
                Example #REJECT 23
                Regards, @KaziMtaani
                """
            resp = self.cancelJob(id,user)
            return resp
        
        elif '#trackjob' in self.text.lower():
            clean_list = self.text.lower().replace('\n','').split('#trackjob')
            id = None
            for i in  clean_list:
                try:
                    inp = int(i)
                    id = inp
                except Exception as e:
                        pass
            if id is None:
                return f"""
                Hey {user.full_name},
                To track your job application please start with the word #TRACKJOB followed by the application id.
                Example #TRACKJOB 23
                Regards, @KaziMtaani
                """
            msg = self.trackJob(id,user)
            return msg
        
        else:
            return f"""
                    Hey {user.full_name},
                    To use this sms service please visit #334*3050# to learn more
                    """
    

    def applyJob(self,id,user):
        try:
            post  = JobPost.objects.get(post_id=id)
            application,_  = JobApplication.objects.get_or_create(jobpost=post,applicant=user) 
           
            return f"""
                 Hi  {user.full_name},
                 Your Application for job {application.jobpost.title} id {application.id} has been processed.
                 We will notify you when we have updates regarding your application status.To track this job applicaton manually reply with
                 #TRACKJOB {application.id} 
                 
                 Thank You!
                 Regards,  @KaziMtaani
                """
        except Exception as e:
            return f"""
                 Hey  {user.full_name},
                 Please ensure that you used an existing job id. We encountered a problem trying to get job id {id}
                 Regards,  @KaziMtaani
                """

    def cancelJob(self,id,user):
        try:
            uid = user.user_id
            application = JobApplication.objects.get(id=id,applicant=uid)
            application.delete()
            return f"""
                    Hey   {user.full_name},
                    Job  Application {id} was cancelled please ensure to double check the job you are applying for to avoid any inconvenience.
                    Regards,  @KaziMtaani
                    """
        except JobApplication.DoesNotExist:
            return f"""
                    Hey {user.full_name},
                    We could not cancel any application id {id} tied to your account
                    """


    def trackJob(self,id,user):
        try:
            uid = user.user_id
            application = JobApplication.objects.get(id=id,applicant=uid)
            return f"""
                        Hey {user.full_name}
                        Your Application Status is {application.status}. Score awarded {application.score} Job  Application {id}                     
                        Regards, @KaziMtaani"""
    
        except JobApplication.DoesNotExist:
            return f"""
                    Hey {user.full_name},
                    We could not find any application id {id} tied to your account
                    """
        

    def rejectMessage(Self):
        return """ 
            Hello ,
            Please Register an account with KaziMtaani by dialing #334*3050# to use this service.
            """

