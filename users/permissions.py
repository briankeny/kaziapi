from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

 
def add_User_To_Group(account_type=None):
    groups  = []
    if account_type:      
        # Define different group names
        recruiterGroup, _ = Group.objects.get_or_create(name='Recruiters')
        jobseekerGroup, _ = Group.objects.get_or_create(name='JobSeekers')

        if account_type.lower() == 'recruiter':
            groups.append(recruiterGroup)
        else:
            groups.append(jobseekerGroup)

    return (groups)