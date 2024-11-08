from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from .ai import AI
from PIL import Image
from io import BytesIO
from .serializers import PromptSerializer

class PromptGemini(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    renderer_classes=[JSONRenderer]
    serializer_class = PromptSerializer
    pagination_class = None

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            image_file = serializer.validated_data.get('image',None)
            prompt = serializer.validated_data.get('prompt',None)

            if prompt == None and image_file == None:
                return Response({'message':'Prompt or Image is missing'},status=status.HTTP_400_BAD_REQUEST)
            if image_file != None:
                image_file = Image.open(image_file)
            
            kazi_ai = AI(image=image_file,prompt=prompt)
            response = kazi_ai.generateAIresponse()

            return Response({'content':response}, status=status.HTTP_200_OK, content_type='application/json')

        except Exception as e:
            print(str(e))
            return Response({'content':'Could not process your request or Service is currently unavailable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')
        