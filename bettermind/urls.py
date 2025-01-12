from django.urls import path


from .views import (
    UserRegistrationAPIView,
    ProfRegistrationAPIView,
    LoginAPIView
)

urlpatterns = [
    path('register/user', UserRegistrationAPIView.as_view(), name='userRegistration'),
    path('register/prof', ProfRegistrationAPIView.as_view(), name="profRegistration"),
    path('login', LoginAPIView.as_view(), name="login"),
]