from django.db import models
from Capstone_users.models import CustomUser

class Subject(models.Model):
    subject_name = models.CharField(max_length=200)

    def __str__(self):
        return self.subject_name

class Question(models.Model):
    CORRECT_ANSWER = (
        ('optionA', 'optionA'),
        ('optionB', 'optionB'),
        ('optionC', 'optionC'),
        ('optionD', 'optionD'),
    )

    subject = models.ForeignKey(Subject, related_name='quiz_subject', on_delete=models.CASCADE)
    question = models.TextField()
    optionA = models.CharField(max_length=200)
    optionB = models.CharField(max_length=200)
    optionC = models.CharField(max_length=200)
    optionD = models.CharField(max_length=200)
    answer = models.CharField(max_length=200, choices=CORRECT_ANSWER) 

    def __str__(self):
        return self.question

class QuizQuestions(models.Model):
    question1 = models.TextField()
    question2 = models.TextField()
    question3 = models.TextField()
    question4 = models.TextField()
    question5 = models.TextField()
    question6 = models.TextField()
    question7 = models.TextField()
    question8 = models.TextField()
    question9 = models.TextField()
    question10 = models.TextField()
    quiz_code = models.CharField(max_length=20)
    created_by = models.ForeignKey(CustomUser, related_name='user_question_creation', on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.quiz_code

class QuizHighScores(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_highscore', on_delete=models.CASCADE)
    quiz_code = models.CharField(max_length=30)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.quiz_code

    class Meta:
        ordering = ('score',)

class UserQuestions(models.Model):
    question1 = models.TextField()
    question2 = models.TextField()
    question3 = models.TextField()
    question4 = models.TextField()
    question5 = models.TextField()
    question6 = models.TextField()
    question7 = models.TextField()
    question8 = models.TextField()
    question9 = models.TextField()
    question10 = models.TextField()
    subject = models.ForeignKey(Subject, related_name='practice_subject', on_delete=models.CASCADE, null=True)
    date_taken = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.question1
