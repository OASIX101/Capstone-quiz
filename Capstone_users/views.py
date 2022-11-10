from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import logout, authenticate
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import PermissionDenied
from Capstone_users.models import CustomUser
from .serializers import LogOutSerializer, LogInSerializer, RegisterSerializer, ChangePasswordSerializer, RegisterSerializer2
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .permissions import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import NotFound

@swagger_auto_schema(method="post",request_body=LogInSerializer())
@api_view(["POST"])
def login_view(request):
    
    if request.method == "POST":
        
        serializer = LogInSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(request, username = serializer.validated_data['username'], password = serializer.validated_data['password'])
        if user:
            if user.is_active:
                try:
                    refresh = RefreshToken.for_user(user)
                    
                    user_details = {}
                    user_details['id']   = user.id
                    user_details['username'] = user.username
                    user_details['refresh_token'] = str(refresh)
                    user_details['access_token'] = str(refresh.access_token)
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                    'message' : "success",
                    'data' : user_details,
                    }
        
                    return Response(data, status=status.HTTP_200_OK)


                except Exception as e:
                    raise e
            
            else:
                data = {
                    'message'  : "failed",
                    'errors': 'This account is not active'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)


        else:
            data = {
                'message'  : "failed",
                'errors': 'Please provide a valid username and password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method="post",request_body=LogOutSerializer())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsUserOrAdmin])
def logout_view(request):
    """Log out a user by blacklisting their refresh token then making use of django's internal logout function to flush out their session and completely log them out.
    Returns:
        Json response with message of success and status code of 204.
    """
    
    serializer = LogOutSerializer(data=request.data)
    
    serializer.is_valid()
    
    try:
        token = RefreshToken(token=serializer.validated_data["refresh_token"])
        token.blacklist()
        user=request.user
        user_logged_out.send(sender=user.__class__,
                                        request=request, user=user)
        logout(request)
        
        return Response({"message": "success"}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({"message": "failed", "error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):

    serializer_class = RegisterSerializer

    @swagger_auto_schema(method='post', request_body=RegisterSerializer())
    @action(methods=['POST'], detail=True)
    def post(self, request):
        user_data = request.data
        if len(user_data['password']) >= 8: 
            serializer = self.serializer_class(data=user_data)
            if serializer.is_valid():
                serializer.save()
                data={
                    'message': 'success',
                }

                return Response(data, status=status.HTTP_201_CREATED)
        
            else:
 
                data={
                    'message': 'failed',
                    'error(s)': serializer.errors,
                }

                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        else:
            raise PermissionDenied(detail={'message': 'password is required to be greater than or equal to 8 characteres'})

class UserEdit(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(id=1)
        except CustomUser.DoesNotExist:
            raise NotFound(detail={'message': 'Permission denied. User does not exist in the database'})

    def get(self, request,  format=None):
        """this endpoint allows logged in user to retrieve their acct details"""
        obj = self.get_user(user_id=request.user.id)
        serializer = RegisterSerializer2(obj)

        data = {
            'message': 'success',
            'data': serializer.data
        }

        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(method='put', request_body=RegisterSerializer2())
    @action(methods=['PUT'], detail=True)
    def put(self, request, format=None):
        """this endpoint allows logged in user to update their acct details"""

        obj = self.get_user(user_id=request.user.id)
        serializer = RegisterSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message': 'success',
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            data = {
                'message': 'failed',
                'error': serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsUserOrAdmin]

    def get_object(self, queryset=None):
        try: 
            return self.request.user
        except CustomUser.DoesNotExist:
            raise PermissionDenied(detail={'message': 'permission denied. user is anonymous.'})

    @swagger_auto_schema(method='patch', request_body=ChangePasswordSerializer())
    @action(methods=['PATCH'], detail=True)
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successful',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='delete')
@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminOnly])
def delete_user(request, user_id):
    """this endpoint allows only admin users to delete a user"""
    try:
        obj = CustomUser.objects.get(id=user_id)  
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        raise NotFound(detail={'message': 'Permission denied. User does not exist in the database'})
   