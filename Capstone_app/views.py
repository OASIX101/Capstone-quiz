from .serializers import *
from rest_framework.decorators import action, authentication_classes, permission_classes, api_view
from rest_framework.exceptions import NotFound, PermissionDenied, NotAcceptable
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from Capstone_users.permissions import *
import string
import random
from datetime import datetime

# Subject views
class SubjectView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, format=None):
        """this endpoint gets all the subjects in the database"""

        subject = Subject.objects.all()
        serializer = SubjectSerializer(subject, many=True)

        data = {
            'message': 'success',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=SubjectSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """this method creates a new subject to the database"""

        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': 'failed to create subject',
                'error(s)': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class SubjectUpdateView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise NotFound(detail={'message': 'Subject with id does not exist.'}) 

    @swagger_auto_schema(method='patch', request_body=SubjectSerializer())
    @action(methods=['PATCH'], detail=True)
    def patch(self, request, subject_id, format=None):
        """this endpoint will update a subject if it exists"""

        obj = self.get_subject(subject_id=subject_id)
        serializer = SubjectSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': 'failed to create subject',
                'error(s)': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, subject_id, format=None):
        """this endpoint will delete a subject if it exists"""

        obj = self.get_subject(subject_id=subject_id)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# Question views
class QuestionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get(self, request, format=None):
        """this endpoint gets all the questions in the database"""

        question = Question.objects.all()
        serializer = QuestionSerializer(question, many=True)

        data = {
            'message': 'success',
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='post', request_body=QuestionSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, format=None):
        """this method creates a new question to the database"""

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': 'failed to create subject',
                'error(s)': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST) 

class QuestionSubjectView(APIView): 

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get(self, request, subject_id, format=None):
        """this endpoint gets all the questions of a given subject in the database if it exists"""
        questions = Question.objects.filter(subject=subject_id)
        if questions.count() > 0:     
            serializer = QuestionSerializer(questions, many=True)

            data = {
                'message': 'success',
                'data': serializer.data,
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            raise NotFound(detail={'message': 'questions under subject not found'})

class QuestionSubjectUpdateView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOnly]

    def get_question(self, question_id):
        try:
            return Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            raise NotFound(detail={'message': 'Question with id does not exist.'}) 

    @swagger_auto_schema(method='put', request_body=QuestionSerializer())
    @action(methods=['PUT'], detail=True)
    def put(self, request, question_id, format=None):
        """this endpoint will update a question if it exists"""

        obj = self.get_question(question_id=question_id)
        serializer = QuestionSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': 'failed to create question',
                'error(s)': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(method='delete')
    @action(methods=['DELETE'], detail=True)      
    def delete(self, request, question_id, format=None):
        """this endpoint will delete a question if it exists"""

        obj = self.get_question(question_id=question_id)
        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

# Quiz Question views
class GroupQuizQuestionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_questions_id(self, qlist):
        questions_id = []
        while len(questions_id) != 10:
            i = random.choice(qlist)
            if i in questions_id:
                continue
            else:
                questions_id.append(i)
        
        return questions_id

    def generate_keycode(self):
        """This function generates random unique passcodes with the integers and certain strings."""

        rand_str = [random.choice(string.ascii_letters) for _ in range(2)]
        code = "".join(rand_str)
        rand_str2 = [random.choice(string.ascii_letters) for _ in range(2)]
        code2 = "".join(rand_str2)
        rand_str3 = [random.choice(string.ascii_letters) for _ in range(2)]
        code3 = "".join(rand_str3)
        today = datetime.now()
        return today.strftime(f"{code2}%d-%m{code3}-{code}%y")

    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise NotFound(detail={'message': 'Subject with id does not exist.'}) 

    def get(self, request, subject_id, format=None):
        """this endpoint generates 10 random question from private group quiz from the subject provided and generates a unique quiz code for accessing the data by users. Allows all users except anonymous users."""

        subject = self.get_subject(subject_id)
        if subject:
            questions_id = []
            for i in Question.objects.filter(subject=subject_id):
                questions_id.append(i.id)
            if len(questions_id) >= 10:
                questions = self.get_questions_id(qlist=questions_id)
                data1 = {}
                num = 0
                for i in questions:
                    num+=1
                    quest = Question.objects.get(id=i)
                    obj = QuestionSerializer2(quest)
                    data1[f'question{num}'] = f'{obj.data}'
                    data1['quiz_code'] = self.generate_keycode()
                    data1['created_by'] = request.user.id
                
                serializer = QuizQuestionsSerializer(data=data1)
                if serializer.is_valid():
                    serializer.save()

                    data = {
                        'message': 'success',
                        'quiz_code': serializer.data['quiz_code']
                    }

                    return Response(data, status=status.HTTP_200_OK)

                else:
                    data = {
                        'message': 'failed',
                        'error(s)': serializer.errors
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'message': 'Questions for this subject in the database is less than 10. Try again later.'})

class GroupQuizView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]
    
    def get_quiz_questions(self, quiz_code):
        try:
            return QuizQuestions.objects.get(quiz_code=quiz_code)
        except QuizQuestions.DoesNotExist:
            raise NotFound(detail={'message': 'Quiz with key code does not exist.'})            

    def get(self, request, quiz_code, format=None):
        """this is endpoint retrieves the generated quiz by the quiz code given"""

        quiz = self.get_quiz_questions(quiz_code)
        serializer = QuizQuestionsSerializer(quiz)

        data = {
            'message': 'success',
            'id': serializer.data['id'],
            'quiz_code': serializer.data['quiz_code'],
            'date_taken': serializer.data['date_taken'],
            'question1': eval(serializer.data['question1']),
            'question2': eval(serializer.data['question2']),
            'question3': eval(serializer.data['question3']),
            'question4': eval(serializer.data['question4']),
            'question5': eval(serializer.data['question5']),
            'question6': eval(serializer.data['question6']),
            'question7': eval(serializer.data['question7']),
            'question8': eval(serializer.data['question8']),
            'question9': eval(serializer.data['question9']),
            'question10': eval(serializer.data['question10']),
        }

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, quiz_code, format=None):
        """this is endpoint deletes the generated quiz by the quiz code given"""

        quiz = self.get_quiz_questions(quiz_code)
        if quiz.created_by == request.user.id:
            quiz.delete()

        else:
            raise PermissionDenied(detail={'message': 'Permission denied. user is not the creator of this quiz'})

@authentication_classes([JWTAuthentication])
@permission_classes([IsUserOrAdmin])
@api_view(['GET'])
def get_quiz_high_scores(request, quiz_code):
    """this endpoint is used to get all the scores for a given quiz"""
    
    if request.method == 'GET':
        obj = QuizHighScores.objects.filter(quiz_code=quiz_code)
        if obj.count() != 0:
            serializer = QuizHighScoreSerializer(obj, many=True)

            data = {
                'message': 'success',
                'data': serializer.data
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            raise NotFound(detail={'message': 'highscores under quiz provided does not exist'})
        
# Quiz Answer views
class QuizAnswerView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_quiz_questions(self, quiz_code):
        try:
            return QuizQuestions.objects.get(quiz_code=quiz_code)
        except QuizQuestions.DoesNotExist:
            raise NotFound(detail={'message': 'Quiz with key code does not exist.'})   

    def user_quiz(self, request, quiz_code):
        try:
            return QuizHighScores.objects.get(quiz_code=quiz_code, user=request.user.id)
        except QuizHighScores.DoesNotExist:
            return None
 
    @swagger_auto_schema(method='post', request_body=QuizAnswerSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, quiz_code, format=None):
        """this endpoint allow users to answer a quiz generated only once provided the quiz code provided is correct"""

        quiz = self.get_quiz_questions(quiz_code)
        if quiz:    
            user = self.user_quiz(request=request, quiz_code=quiz_code)
            serializer = QuizAnswerSerializer(data=request.data)
            if user is None:
                if serializer.is_valid():
                    score = 0
                    correct_answers = {}
                    score_data = {}
                    if request.data.get('answer1') == eval(quiz.question1)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question1'] = eval(quiz.question1)['answer']

                    if request.data.get('answer2') == eval(quiz.question2)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question2'] = eval(quiz.question2)['answer']

                    if request.data.get('answer3') == eval(quiz.question3)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question3'] = eval(quiz.question3)['answer']

                    if request.data.get('answer4') == eval(quiz.question4)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question4'] = eval(quiz.question4)['answer']

                    if request.data.get('answer5') == eval(quiz.question5)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question5'] = eval(quiz.question5)['answer']

                    if request.data.get('answer6') == eval(quiz.question6)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question6'] = eval(quiz.question6)['answer']

                    if request.data.get('answer7') == eval(quiz.question7)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question7'] = eval(quiz.question7)['answer']

                    if request.data.get('answer8') == eval(quiz.question8)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question8'] = eval(quiz.question8)['answer']

                    if request.data.get('answer9') == eval(quiz.question9)['answer']:
                        score += 1
                    else:
                        correct_answers['answer_for_question9'] = eval(quiz.question9)['answer']

                    if request.data.get('answer10') == eval(quiz.question10)['answer']:
                        score += 1    
                    else:
                        correct_answers['answer_for_question10'] = eval(quiz.question10)['answer']  

                    score_data['score'] = score
                    score_data['quiz_code'] = quiz_code
                    score_data['user'] = request.user.id
                    serializer2 = QuizHighScoreSerializer(data=score_data)
                    if serializer2.is_valid():
                        serializer2.save()
                        data = {
                            'user': request.user.id, 
                            'quiz_code': quiz_code,
                            'score': score,
                            'correction(s)': correct_answers,
                            'date_taken': datetime.now()
                        }

                        return Response(data=data, status=status.HTTP_200_OK)
                    else:
                        data = {
                            'message': 'failed',
                            'error(s)': serializer2.errors
                        }
                        return Response(data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    data = {
                        'message': 'failed',
                        'error(s)': serializer.errors
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                raise PermissionDenied(detail={'message': 'user cannot answer this question twice'})

# user practice views
class UserQuestionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise NotFound(detail={'message': 'Subject with id does not exist.'}) 

    def get_questions_id(self, qlist):
        questions_id = []
        while len(questions_id) != 10:
            i = random.choice(qlist)
            if i in questions_id:
                continue
            else:
                questions_id.append(i)
        
        return questions_id

    def get(self, request, subject_id, format=None):
        """this endpoint generate 10 random questions from the subject provided for user practice. Allows all users except anonymous users"""

        subject = self.get_subject(subject_id)
        if subject:
            questions_id = []
            for i in Question.objects.filter(subject=subject_id):
                questions_id.append(i.id)
            if len(questions_id) >= 10:
                questions = self.get_questions_id(qlist=questions_id)
                data1 = {}
                num = 0
                for i in questions:
                    num+=1
                    quest = Question.objects.get(id=i)
                    obj = QuestionSerializer2(quest)
                    data1[f'question{num}'] = f'{obj.data}'
                    data1['created_by'] = request.user.id
                    data1['subject'] = subject_id
                
                serializer = UserQuestionSerializer(data=data1)
                if serializer.is_valid():
                    serializer.save()

                    data = {
                        'message': 'success',
                        'questions': serializer.data
                    }

                    return Response(data, status=status.HTTP_200_OK)

                else:
                    data = {
                        'message': 'failed',
                        'error(s)': serializer.errors
                    }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'message': 'Questions for this subject in the database is less than 10. Try again later.'})

class UserAnswerQuestionView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_questions(self, question_id):
        try:
            return UserQuestions.objects.get(id=question_id)
        except UserQuestions.DoesNotExist:
            raise NotFound(detail={'message': 'Quiz with key code does not exist.'})

    @swagger_auto_schema(method='post', request_body=QuizAnswerSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request, question_id, format=None):
        """this endpoint allows users to answer practice questions"""
        quiz = self.get_questions(question_id)
        if quiz:    
            serializer = QuizAnswerSerializer(data=request.data)
            if serializer.is_valid():
                score = 0
                correct_answers = {}
                if request.data.get('answer1') == eval(quiz.question1)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question1'] = eval(quiz.question1)['answer']

                if request.data.get('answer2') == eval(quiz.question2)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question2'] = eval(quiz.question2)['answer']

                if request.data.get('answer3') == eval(quiz.question3)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question3'] = eval(quiz.question3)['answer']

                if request.data.get('answer4') == eval(quiz.question4)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question4'] = eval(quiz.question4)['answer']

                if request.data.get('answer5') == eval(quiz.question5)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question5'] = eval(quiz.question5)['answer']

                if request.data.get('answer6') == eval(quiz.question6)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question6'] = eval(quiz.question6)['answer']

                if request.data.get('answer7') == eval(quiz.question7)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question7'] = eval(quiz.question7)['answer']

                if request.data.get('answer8') == eval(quiz.question8)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question8'] = eval(quiz.question8)['answer']

                if request.data.get('answer9') == eval(quiz.question9)['answer']:
                    score += 1
                else:
                    correct_answers['answer_for_question9'] = eval(quiz.question9)['answer']

                if request.data.get('answer10') == eval(quiz.question10)['answer']:
                    score += 1    
                else:
                    correct_answers['answer_for_question10'] = eval(quiz.question10)['answer']  

                data = {
                    'user': request.user.id, 
                    'subject': quiz.subject.id,
                    'score': score,
                    'correction(s)': correct_answers,
                    'date_taken': datetime.now()
                }

                return Response(data=data, status=status.HTTP_200_OK)

            else:
                data = {
                    'message': 'failed',
                    'error(s)': serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)