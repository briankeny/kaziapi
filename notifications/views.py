from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.response import Response
from .models import (Notification)
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer,NotificationDetailedSerializer
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination


class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)
    renderer_classes=[JSONRenderer]
    serializer_class = NotificationDetailedSerializer
    pagination_class = LimitOffsetPagination 

    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(user=user)
        # Optional search term filtering
        search_term = str(self.request.query_params.get('searchTerm', None))
        search = str(self.request.query_params.get('search', None))
        # Sort order based on newer ones        
        queryset = queryset.order_by('timestamp')          
      
        if search_term != 'None' and search != 'None':
            try:
                field = f'{search_term}__icontains'
                # UsING filter() for case-insensitive search using icontains
                queryset = queryset.filter(**{field: search})
            except Exception as e:
                    queryset = []
        return queryset


# This View is For Changing Nofitifications 
class NotificationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notification.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    renderer_classes=[JSONRenderer]
    serializer_class = NotificationSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        user = self.request.user 
        notification = self.get_object()

        if user.user_id != notification.user.user_id:
             return Response({}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
         return Response({'message': 'Unsupported Request or Method Not Allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        notification = self.get_object()

        if user.user_id != notification.user.user_id:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        notification.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT, content_type='application/json')
