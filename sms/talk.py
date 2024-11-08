# works with both python 2 and 3
from __future__ import print_function
from kaziapi import settings
import africastalking

class SMS:
    def __init__(self, recipients, message):
		# Set your app credentials
        self.username = settings.SMS_USERNAME
        self.api_key = settings.SMS_API_KEY
        self.message = message
        self.recipients = recipients

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self):
            # Set your shortCode or senderId
            sender = settings.SMS_NUMBER
            try:
				# Thats it, hit send and we'll take care of the rest.
                response = self.sms.send(self.message,self.recipients, sender)
                # print(f'Raw response is {response}')
                return response
            except Exception as e:
                # print ('Encountered an error while sending: %s' % str(e))
                return {'ok':False, 'error':str(e)}

