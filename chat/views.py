from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions,status
from .models import Message, Chat
from .serializers import MessageSerializer, ChatSerializer,ChatWithParticipantsSerializer
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
from users.models import User

class ChatList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Chat.objects.all()
    serializer_class = ChatWithParticipantsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination 

    # Filter Chats based on user
    def get_queryset(self):
        user = self.request.user
        queryset =Chat.objects.filter(participants=user.user_id)
        return queryset

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset= Message.objects.all()
    pagination_class = LimitOffsetPagination 

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        chat = get_object_or_404(Chat, pk=chat_id)
        return Message.objects.filter(conversation=chat)

class MessageCreate(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes=(MultiPartParser,)
    

    # Create
    def create(self, request, *args, **kwargs):
        user = self.request.user
        data = request.data.copy()
        receiver = data.get('receiver',None)

        if receiver == None:
            return Response({'error':'Missing Credentials'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            id= int(receiver)
            receiver = User.objects.get(user_id=id)
        except Exception as e:
            return Response({'error':'Missing Credentials'},status=status.HTTP_400_BAD_REQUEST)

        if receiver.user_id == user.user_id:
            return Response({'error':'You cannot send a message to yourself'},status=status.HTTP_400_BAD_REQUEST)
    
       # Check if a chat with these participants already exists
        participants = [receiver.user_id,user.user_id]
        chat = Chat.objects.filter(participants__in=participants).first()
        print(f'CHat is {chat.chat_id} ')

        # If no existing chat, create a new one
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(user, receiver)
            chat.save()

        data['sender'] = user.user_id
        data['conversation'] = chat.chat_id

        #serialize data 
        serializer = self.get_serializer(data=data, partial=True)

        # Check if serializer data is valid
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data,status=status.HTTP_201_CREATED)

class MessageDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Dissallow unsafe methods
    def put(self, request, *args, **kwargs):
         return Response({'message': 'Unsupported Request.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
     # Dissallow unsafe methods
    def patch(self, request, *args, **kwargs):
         return Response({'message': 'Unsupported Request.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_queryset(self):
        chat_id = self.kwargs['pk']
        Chat = get_object_or_404(Chat, pk=chat_id)
        return Message.objects.filter(Chat=Chat)

    # Accept Delete Method
    def delete(self, request, *args, **kwargs):
        user = self.request.user
        message = self.get_object()
        
        # Check if the message belongs to this requester or is authorized
        if not (message.sender.user_id == user.user_id) or not user.is_superuser:
           return Response({'error':'You are not allowed to peform this operation'}, status=status.HTTP_423_LOCKED)
        message.delete()
        #Delete was successful return response
        return Response({}, status=status.HTTP_204_NO_CONTENT)
        
    
    