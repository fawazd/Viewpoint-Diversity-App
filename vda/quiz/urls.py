from django.urls import path
from django.conf.urls import url

from . import views
from quiz.views import HomeView, QuizView, ProgressView

app_name = 'quiz'

########## URls to the three HTML templates and what Views they use ##########

urlpatterns = [
    #When use is directed to a page, the page id is passed to and from the view and the template through the URL.
    path('quiz/<int:page_id>/', QuizView.as_view(), name='quiz'),
    path('quiz/', QuizView.as_view(), name='quiz_post'),
    path('', HomeView.as_view(), name='index'),
    path('progress/', ProgressView.as_view(), name='progress'),
]
