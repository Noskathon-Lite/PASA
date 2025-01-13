from django.urls import path

from .views import (
    UserRegistrationAPIView,
    ProfRegistrationAPIView,
    LoginAPIView,
    UserAnswerSubmitAPIView,
    ProfAnswerSubmitAPIView,
    get_agora_token,
    save_proffcm_token,
    save_userfcm_token,
)

urlpatterns = [
    path('register/user', UserRegistrationAPIView.as_view(), name='userRegistration'),
    path('register/prof', ProfRegistrationAPIView.as_view(), name="profRegistration"),
    path('login', LoginAPIView.as_view(), name="login"),
    path('answer/user', UserAnswerSubmitAPIView.as_view(), name="userAnswer"),
    path('answer/prof', ProfAnswerSubmitAPIView.as_view(), name="profAnswer"),
    path('getToken/', get_agora_token, name='getAgoraToken'),
    path('savefcm/user', save_userfcm_token, name="saveUserFcm"),
    path('savefcm/prof', save_proffcm_token, name="saveProfFcm"),
]