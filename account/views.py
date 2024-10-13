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
    """
    Renders the homepage.
    No authentication is required to access this view.
    """
    permission_classes = []  # No authentication required

    def get(self, request, format=None):
        """
        Handles GET requests to render the home page.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered home.html template.
        """
        return render(request, 'home.html')

def get_tokens_for_user(user):
    """
    Generates JWT tokens for the authenticated user.

    Args:
    - user: The authenticated user instance.

    Returns:
    - A dictionary with 'refresh' and 'access' tokens.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class UserLoginView(APIView):
    """
    Manages the user login functionality.
    """
    permission_classes = []

    def get(self, request, format=None):
        """
        Renders the login page for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered login.html template.
        """
        return render(request, 'login.html')

    def post(self, request, format=None):
        """
        Handles user login for POST requests.

        Args:
        - request: The HTTP request object with login data.

        Returns:
        - Redirects to the dashboard if successful, or renders login.html with form errors.
        """
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)  # Log the user in
                return redirect('dashboard')
            else:
                return render(request, 'login.html', {'form_errors': {'non_field_errors': ['Email or Password is not valid']}})
        else:
            return render(request, 'login.html', {'form_errors': serializer.errors})



class UserRegistrationView(APIView):
    """
    Manages the user registration process.
    """
    permission_classes = []
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        """
        Renders the registration form for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered signup.html template.
        """
        return render(request, 'signup.html')

    def post(self, request, format=None):
        """
        Handles user registration for POST requests.

        Args:
        - request: The HTTP request object with registration data.

        Returns:
        - Redirects to the login page upon successful registration, or renders signup.html with form errors.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')  # Redirect to login after successful registration
        return render(request, 'signup.html', {'form_errors': serializer.errors})


class UserProfileView(APIView):
    """
    Displays the profile of the authenticated user.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Handles GET requests to display the user profile.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered profile.html template with user profile data.
        """
        serializer = UserProfileSerializer(request.user)
        return render(request, 'profile.html', {'user': serializer.data})



class UserChangePasswordView(APIView):
    """
    Allows authenticated users to change their password.
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """
        Renders the change password form for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered change_password.html template.
        """
        return render(request, 'change_password.html')

    def post(self, request, format=None):
        """
        Handles password change for authenticated users.

        Args:
        - request: The HTTP request object with password change data.

        Returns:
        - JSON response indicating success or failure.
        """
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailView(APIView):
    """
    Sends a password reset email to the user.
    """
    permission_classes = []
    renderer_classes = [UserRenderer]

    def get(self, request, format=None):
        """
        Renders the password reset email form for GET requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Rendered password_reset_email.html template.
        """
        return render(request, 'password_reset_email.html')

    def post(self, request, format=None):
        """
        Sends a password reset link to the user's email.

        Args:
        - request: The HTTP request object with the email data.

        Returns:
        - JSON response indicating the email was sent.
        """
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset link sent. Please check your email.'}, status=status.HTTP_200_OK)



class UserPasswordResetView(APIView):
    """
    Handles the password reset process using a token sent to the user's email.
    """
    renderer_classes = [UserRenderer]

    def get(self, request, uid, token, format=None):
        """
        Renders the password reset form for GET requests.

        Args:
        - request: The HTTP request object.
        - uid: The user's ID.
        - token: The password reset token.

        Returns:
        - Rendered reset_password.html template.
        """
        return render(request, 'reset_password.html', {'uid': uid, 'token': token})

    def post(self, request, uid, token, format=None):
        """
        Resets the user's password based on the token provided.

        Args:
        - request: The HTTP request object with the new password data.
        - uid: The user's ID.
        - token: The password reset token.

        Returns:
        - JSON response indicating the password was reset successfully.
        """
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid': uid, 'token': token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg': 'Password reset successfully'}, status=status.HTTP_200_OK)



class LogoutView(APIView):
    """
    Logs the user out and clears the session.
    """
    def post(self, request):
        """
        Handles user logout for POST requests.

        Args:
        - request: The HTTP request object.

        Returns:
        - Redirects to the login page after logout.
        """
        logout(request)
        request.session.flush()  # Clear session data
        return redirect('login')