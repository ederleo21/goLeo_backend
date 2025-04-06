from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, UserProfileView, send_contact_email
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/user/register/", CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path("profile/", UserProfileView.as_view(), name='user-profile'),
    path("core/", include('core.urls')),
    path("tournaments/", include('tournaments.urls')),  
    path("performance/", include('performance.urls')),  
    path("send-email/", send_contact_email, name="send_email")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                                