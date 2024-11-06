import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from jobs.models import JobPost, Job, User  # Replace 'myapp' with your app name

fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample job posts'

    def add_arguments(self, parser):
        parser.add_argument(
            '--total', type=int, default=10,
            help='Number of job posts to create'
        )

    def handle(self, *args, **options):
        total = options['total']
        employment_choices = [choice[0] for choice in JobPost.EMPLOYMENT_CHOICES]
        experience_choices = [choice[0] for choice in JobPost.EXPERIENCE_CHOICES]
        status_choices = [choice[0] for choice in JobPost.STATUS_CHOICES]

        # Get available categories and recruiters
        categories = list(Job.objects.all())
        recruiters = list(User.objects.all())

        if not categories or not recruiters:
            self.stdout.write(self.style.ERROR('Please ensure there are categories and users in the database.'))
            return

        for _ in range(total):
            job_post = JobPost(
                category=random.choice(categories),
                title=fake.job(),
                description=fake.paragraph(nb_sentences=5),
                location=fake.city(),
                employment_type=random.choice(employment_choices),
                experience_level=random.choice(experience_choices),
                salary_range=f"{fake.random_int(min=30000, max=120000)}-{fake.random_int(min=130000, max=200000)}",
                recruiter=random.choice(recruiters),
                impressions=fake.random_int(min=0, max=1000),
                status=random.choice(status_choices),
                deadline_date=timezone.now() + timezone.timedelta(days=random.randint(1, 30)),
                longitude=fake.longitude(),
                latitude=fake.latitude()
            )
            
            job_post.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully created job post: {job_post.title}'))
