from django.urls import path

from users.views.user_signup import UserSignUpView


"""
유저 회원가입 url patterns
"""
urlpatterns = [
    path('/signup', UserSignUpView.as_view()),
]