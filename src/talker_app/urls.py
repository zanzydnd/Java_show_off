from django.urls import path

from talker_app.views import registration, AuthView, home_page, logout_view, create_talk_view, profile_view, talk_view, \
    answer_view

urlpatterns =[
    path("",home_page,name="home"),
    path("profile/<str:username>",profile_view,name="profile"),
    path("logout",logout_view,name="logout"),
    path('registration/',registration,name="registration"),
    path('auth/',AuthView.as_view(),name="login"),
    path('create/',create_talk_view,name="talk_create"),
    path('talk/<int:talk_id>',talk_view,name = "talk_page"),
    path('answer/<int:talk_id>',answer_view,name="answer"),
]