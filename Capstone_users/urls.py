from django.urls import path, include
from . import views

urlpatterns = [
    path('access/', include('djoser.urls.jwt')),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('register/', views.RegisterView().as_view()),
    path('user-details/', views.UserEdit().as_view(), name="user_details"),
    path('user-reset-password/', views.ChangePasswordView().as_view(), name="user_reset_password"),
    path('user-delete/<int:user_id>/', views.delete_user, name="user_delete"),
]