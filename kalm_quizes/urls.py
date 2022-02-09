from django.urls import path
from . import views

app_name = 'kalm_quizes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('course<int:quiz_id>/', views.quiz_page, name='quiz_page'),
    path('course<int:quiz_id>/singlechoice<int:single_choice_id>/',
         views.single_choice_page, name='single_choice_page'),
    path('course<int:quiz_id>/singlechoice<int:single_choice_id>/check',
         views.single_choice_page, name='single_choice_page'),
    path('course<int:quiz_id>/ordering<int:put_in_order_id>/',
         views.put_in_order_page, name='put_in_order_page'),
    path('course<int:quiz_id>/ordering<int:put_in_order_id>/check',
         views.put_in_order_check, name='put_in_order_checking'),
]
