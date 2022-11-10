from django.urls import path
from . import views

urlpatterns = [
    path('question/', views.QuestionView().as_view(), name='question'),
    path('questions/<int:subject_id>/', views.QuestionSubjectView().as_view(), name='question_subject'),
    path('question/<int:question_id>/', views.QuestionSubjectUpdateView().as_view(), name='question_subject_update'),
    path('subject/', views.SubjectView().as_view(), name='subject'),
    path('subject/<int:subject_id>/', views.SubjectUpdateView().as_view(), name='subject_update'),
    path('generate-quiz/<int:subject_id>/', views.GroupQuizQuestionView().as_view(), name='group_quiz'),
    path('group-quiz/<str:quiz_code>/', views.GroupQuizView().as_view(), name='Group_quiz_view'),
    path('answer-quiz/<str:quiz_code>/', views.QuizAnswerView().as_view(), name='answer_quiz'),
    path('user-practice/<int:subject_id>/', views.UserQuestionView().as_view(), name='user_practice'),
    path('answer-practice/<int:question_id>/', views.UserAnswerQuestionView().as_view(), name='answer_practice'),
    path('quiz-highscores/<str:quiz_code>/', views.get_quiz_high_scores, name='quiz_highscores'),
]