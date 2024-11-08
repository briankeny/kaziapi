from django.urls import path
from .views import PromptGemini

urlpatterns = [
    path('prompt-kaziMtaani-AI/', PromptGemini.as_view(), name='kazi-prompt-ai'),
]
