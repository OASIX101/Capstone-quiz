# Capstone-quiz

Super user credentials = {
    'username': 'oasix',
    'password': 'oreoluwa'
}


                                                        ---EXPLANATION---

    I created a quiz api that registers users and allows users to change their password only when they are logged in(I didnt add an endpoint that allows users to change their password when they are not logged in because i didnt implement user email verification for a reason which is that you are able create a new user and test the api without going through that verification step). The api also allows users to get questions related to the subject provided which the condition that the subject exists in the database. It allows users to generate 10 random questions for private group quiz (like Kahoot.io that was used on the graduation day) which the quiz questions can be accessed by a unique quiz code generated for each group quiz created and allow users to only be able to answer the quiz once. Its allow give room for users to be able to practice questions which are 10 randomly generated questions. The frontend development is supposed to ask the user a how many questions they would like to answer with some limitations on how many they must not exceed and get random questions without repetitions of questions but i made those endpoints cos i didnt know you wanted me to do the quis api.

                                                        ---ENDPOINTS---
-question/ : allows only admin users to get all the questions and create new questions.

-questions/<int:subject_id>/ : allows only admin users to get all the questions related to the given subject.

-question/<int:question_id>/ : allows only admin users to update and delete the given question id.

subject/ : allows only admin users to add a ne1 subject but allows all users to get the subjects in the database.

-subject/<int:subject_id>/ : allows only admin users to update and delete the subject provided

-generate-quiz/<int:subject_id>/ : allows users to generate 10 random questions and quiz code for accessing the quiz for private group quiz. 

-group-quiz/<str:quiz_code>/ : it allows users to get the questions generated provided the quiz code given exists ans delete the quiz if the user that created the quiz is the one that wants to delete the quiz.


-answer-quiz/<str:quiz_code>/ : allows users to answer a private group quiz provided the quiz code given exists and user has not answered quiz before

-user-practice/<int:subject_id>/ : allows users to generate 10 random questions to practice

-answer-practice/<int:question_id>/ : allows users to answer practice questions.

-quiz-highscores/<str:quiz_code>/ : allows users to get the all the scores for a given private quiz.

-user-reset-password/ : allows logged in users to reset theior password

-user-delete/<int:user_id>/ : allows only admin do delete a user.

-user-details/: allows logged in users to get and update user details.

-register/ : to register user.
