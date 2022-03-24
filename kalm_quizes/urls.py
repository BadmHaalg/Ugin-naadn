from django.urls import path
from . import views

app_name = 'kalm_quizes'
urlpatterns = [
    path('', views.index_page, name='index'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('about/', views.about_page, name='about'),
    path('profile/', views.profile_page, name='profile'),
    path('glossary/', views.glossary_page, name='glossary'),
    path('course<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    path('course<int:quiz_id>/singlechoice<int:question_id>/',
         views.single_choice_page, name='single_choice_page'),
    path('course<int:quiz_id>/ordering<int:question_id>/',
         views.put_in_order_page, name='put_in_order_page'),
    path('course<int:quiz_id>/gaps<int:question_id>/',
         views.put_in_gaps_page, name='put_in_gaps_page'),
    ]
