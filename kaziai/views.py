# from django.shortcuts import render

# # Create your views here.

# class PromptGemini(generics.CreateAPIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     parser_classes = (MultiPartParser,)
#     renderer_classes=[JSONRenderer]
#     serializer_class = PromptSerializer
#     pagination_class = None

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.serializer_class(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             image_file = serializer.validated_data.get('image',None)
#             prompt = serializer.validated_data.get('prompt',None)

#             if prompt == None:
#                 return Response({'message':'Prompt Message is missing'},status=status.HTTP_400_BAD_REQUEST)

#             model_name = 'gemini-pro'

#             if image_file != None:
#                 # Process the image filedrf-yasgdrf-yasg


#                 try:
#                     image = Image.open(image_file)
#                     model_name = 'gemini-pro-vision'
#                     model = genai.GenerativeModel(model_name)
#                     response = model.generate_content([prompt, image], stream=False)
#                 except Exception as e:
#                     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#             else:
#                 model = genai.GenerativeModel(model_name)
#                 response = model.generate_content(prompt)
#             response.resolve()
#             # my_json = to_markdown(response.text)
#             # print(my_json)
#             # airesp = json.dumps(my_json)

#             return Response({'content':response.text}, status=status.HTTP_200_OK, content_type='application/json')

#         except Exception as e:
#             print(str(e))
#             return Response({'message':'Service is currently unavailable'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type='application/json')


