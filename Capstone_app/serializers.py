from rest_framework import serializers
from .models import *

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

class QuestionSerializer2(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ['question', 'optionA', 'optionB', 'optionC', 'optionD', 'answer']

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = '__all__'

class QuizQuestionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizQuestions
        fields = '__all__'    

class QuizAnswerSerializer(serializers.Serializer):
    OPTIONS = (
        ('optionA', 'optionA'),
        ('optionB', 'optionB'),
        ('optionC', 'optionC'),
        ('optionD', 'optionD'),
    )


    answer1 = serializers.ChoiceField(choices=OPTIONS)
    answer2 = serializers.ChoiceField(choices=OPTIONS)
    answer3 = serializers.ChoiceField(choices=OPTIONS)
    answer4 = serializers.ChoiceField(choices=OPTIONS)
    answer5 = serializers.ChoiceField(choices=OPTIONS)
    answer6 = serializers.ChoiceField(choices=OPTIONS)
    answer7 = serializers.ChoiceField(choices=OPTIONS)
    answer8 = serializers.ChoiceField(choices=OPTIONS)
    answer9 = serializers.ChoiceField(choices=OPTIONS)
    answer10 = serializers.ChoiceField(choices=OPTIONS)
  
class QuizHighScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuizHighScores
        fields = '__all__'

class UserQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserQuestions
        fields = '__all__'