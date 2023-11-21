from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="Home_Page"),
    path('api/create-question/', views.createQuestion, name="Create_Question"),
    path('api/question-store/', views.questionStore, name="Question_Store"),
    path('api/generate-question-paper/', views.generateQuestionPaper, name="Generate_Question_Paper"),
    # path('update', views.updateQuestionMarks)
]
