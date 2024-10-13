from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,UserPasswordResetSerializer
from account.renderers import UserRenderer
from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class HomePageView(APIView):
    permission_classes = []  # No authentication required

    def get(self, request, format=None):
        return render(request, 'home.html')


def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
  }




class UserLoginView(APIView):
    permission_classes = []
    def get(self, request, format=None):
        return render(request, 'login.html')

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)  # Logs the user in
                print(f"User authenticated: {user.is_authenticated}")  # Debug log
                return redirect('dashboard')  # Redirect to dashboard after successful login
            else:
                return render(request, 'login.html', {'form_errors': {'non_field_errors': ['Email or Password is not Valid']}})
        else:
            return render(request, 'login.html', {'form_errors': serializer.errors})

class UserRegistrationView(APIView):
    permission_classes = []
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        return render(request, 'signup.html')  # Renders the signup page

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # Save the user data to the database
            return redirect('login')  # Redirect to login page after successful registration
        else:
            # In case of errors, render the signup page again with form errors
            return render(request, 'signup.html', {'form_errors': serializer.errors})
 # Renders form errors on the signup page


class UserProfileView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    serializer = UserProfileSerializer(request.user)
    return render(request, 'profile.html', {'user': serializer.data})  # Renders profile template


class UserChangePasswordView(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]

  def get(self, request, format=None):
    return render(request, 'change_password.html')  # Renders password change form

  def post(self, request, format=None):
    serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
  renderer_classes = [UserRenderer]

  def get(self, request, format=None):
    return render(request, 'password_reset_email.html')  # Renders email form

  def post(self, request, format=None):
    serializer = SendPasswordResetEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Reset link sent. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
  renderer_classes = [UserRenderer]

  def get(self, request, uid, token, format=None):
    return render(request, 'reset_password.html', {'uid': uid, 'token': token})  # Renders reset password form

  def post(self, request, uid, token, format=None):
    serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
    serializer.is_valid(raise_exception=True)
    return Response({'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)



class LogoutView(APIView):
    def post(self, request):
        logout(request)
        # Clear any stored search/selection state
        request.session.flush()
        return redirect('login')