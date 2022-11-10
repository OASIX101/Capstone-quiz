from django.contrib import admin
from .models import *

admin.site.register([Question, QuizHighScores, QuizQuestions, Subject, UserQuestions])
