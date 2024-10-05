from django.shortcuts import render

# Create your views here.
class JobListCreate(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class ApplicationListCreate(generics.ListCreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class SkillListCreate(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class SkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class JobSkillListCreate(generics.ListCreateAPIView):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer

class JobSkillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobSkill.objects.all()
    serializer_class = JobSkillSerializer

class SavedJobListCreate(generics.ListCreateAPIView):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer

class SavedJobDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedJob.objects.all()
    serializer_class = SavedJobSerializer

class ReviewListCreate(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer