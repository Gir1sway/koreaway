from django.conf.urls.static import static
from django.contrib.auth import views
from django.urls import path

from Computer_market import settings
from .forms import UserLoginForm
from .views import RegisterView, CustomLoginView

urlpatterns = [
    path("signup/", RegisterView.as_view(template_name='registration/registration.html'),
         name="signup"),
    path('login/', CustomLoginView.as_view(template_name="registration/login.html"),
         name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
