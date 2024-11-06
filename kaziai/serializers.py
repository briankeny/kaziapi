from rest_framework import serializers

class PromptSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    prompt = serializers.CharField()
    
    class Meta:
        fields = ['image', 'prompt']


