from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from django.conf import settings

# Apps urls
import authentication.urls as auth_urls
import notifications.urls as notification_urls
import users.urls as user_urls
import chat.urls as chat_urls
import jobs.urls as jobs_urls
import recovery.urls as recov_urls
import sms.urls as smurls

# import reports.urls as repurls
# from rest_framework_swagger.views import get_swagger_view

# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Roads API",
#         default_version="v1",
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # path('', include(repurls)),
    path('', include(notification_urls)),
    path('', include(auth_urls)),
    path('', include(recov_urls)),
    path('', include(smurls)),
    path('', include(user_urls)),
    path('', include(jobs_urls)),
    path('', include(chat_urls)),
    path('admin/', admin.site.urls),
    # path('swagger/',schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui")
]

# Add this line to serve media files during development
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
