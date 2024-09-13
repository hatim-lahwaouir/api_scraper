from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSignUp, UserInfo
from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

# create the token 

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




@api_view(['POST'])
@permission_classes([AllowAny])
def signUp(request):
    userSerializer = UserSignUp(data=request.data)
    if not userSerializer.is_valid():
        return Response(userSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
    userSerializer.save()

    return Response({"message" : "Account created !"})
        




@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email', '')
    password = request.data.get('password', '')

    user = User.objects.filter(email=email).first()

    if user is None or not user.check_password(password) :
        return Response({"message" : "Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)


    userInfo = UserInfo(user)
    return Response({"message" : "Login Successful!", 'tokens': get_tokens_for_user(user), "info" : userInfo.data})

