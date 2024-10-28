from django.conf import settings
from users.models import User
from jobs.models import Job,JobApplication
from .signals import send_job_enquiries_to_client,send_job_applications_to_client

class KaziUSSDMessages:

    def __init__(self,username):
        self.username = username
        self.message=''

        pass

    def welcomeInterfaceMessage(self):
        self.message = """CON 
        Welcome to Kazi Mtaani!
        1. I want to register account
        2. I have an Account
        """
        return self.message
    
    # First Level (1)
    # End here
    def registerInterfaceMessage(self):
        self.message =  """END 
        To create an account with KaziMtaani download our app and register or follow instructions that will be sent to you shortly. 
        Thank You!
        """
        return self.message
    
    # First Level Option 2
    # One level up option (2)
    def accountMessage(self):
        self.message =  f"""CON 
        Hi {self.username}! What can we do for you?
        1. Apply for a job
        2. Check application status
        """

        return self.message

    # Second Level levels up (2*1)
    #option 1 
    def listJobsMessage(self):
        self.message = f"""END 
        Hi {self.username},
        You will receive an sms shortly with jobs matching your profession.
        Please reply with a job number of your choice to 30508 starting with #APPLYJOB.
        Thank You!
        """
        return self.message
    
    # Second levels up(2*2)
    # Option 2
    def sendApplicationMessage(self):
        self.message = f"""END Hi {self.username},
        We will send you a brief sms shortly with an application status for your recent jobs.
        Thank You!
        """
        return self.message

    # Rejection message
    def rejectMessage(self):
        self.message ="""END We are unable to process your request at the moment please try again later.
        Thank You! 
        """
        return self.message

class KaziUSSDActions(KaziUSSDMessages):

    def __init__(self,phoneNumber,text,sender):
        self.phoneNumber = phoneNumber
        self.text = text
        self.message= ''
        self.username = ''
        self.jobs=[]
        self.sender = sender
        # sessionId = data.get('text',None)
        # serviceCode  = self.serviceCode

    def switchAction(self):
        
        if self.text == '' :
            # Send welcome interface message  
            return self.welcomeInterfaceMessage()

        # First Level Response
        elif self.text == '1':
            # Send Register User Message
            return self.registerInterfaceMessage()
            
        elif self.text == '2':
            # Check if a user has an existing account
            try:

                user = User.objects.get(mobile_number=self.phoneNumber)
                print(f'found user {user.full_name}')
                if user:
                    uname= user.full_name
                    self.username = uname[:15]
                    return self.accountMessage()
    
            except User.DoesNotExist:
                #Send User Registration message
                return self.registerInterfaceMessage()
            
        # Second level up
        # Business
        elif self.text == '2*1':
            # Check if a user has an existing account
            try:
                user = User.objects.get(mobile_number=self.phoneNumber)

                # If a user has an account
                if user:
                    uname= user.full_name
                    self.username = uname[:15]
                    send_job_enquiries_to_client.send(
                        sender=self.sender,
                        instance=user,
                        recepient = self.phoneNumber
                        )
                    return self.listJobsMessage()
    
            except User.DoesNotExist:
                #Send User Registration message
                return self.registerInterfaceMessage()
            
        elif self.text == '2*2':
            # Check if a user has an existing account
            try:
                user = User.objects.get(mobile_number = self.phoneNumber)
                if user:
                    uname= self.username
                    self.username = uname[:15]
                    # Send Application Message
                    send_job_applications_to_client.send(
                        sender=self.sender,
                        instance=user,
                        recepient = self.phoneNumber
                        )
                    return self.sendApplicationMessage()
    
            except User.DoesNotExist:
                #Send User Registration message
                return self.registerInterfaceMessage()
            
        else:
            # send rejection message
            return self.rejectMessage()

            


        