from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password




class UserInfo(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "id", "contact"]


class UserSignUp(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "contact"]

    
    def validate_username(self, value:str):
        value = value.strip()
        if len(value) < 3 or len(value) > 40:
            raise serializers.ValidationError("Usernmae max length is 40, and min length is 3")
        if not value.isalnum():
            raise serializers.ValidationError("Usernmae can only include  digits and alpha")

        return value

    def validate_email(self, value:str):
        
        print(value)
        if not ('.' in value and '@' in value):
            raise serializers.ValidationError("Invalid email")
        return value
    


    def validate_password(self, value:str):

        if len(value) < 10:
            raise serializers.ValidationError("Min password length is 10")

        return make_password(value)



    def validate_contact(self, value:str):
        
        if not value.isdigit():
            raise serializers.ValidationError("Contact must contain only digits")

        if len(value) < 10 or len(value) > 15:
            raise serializers.ValidationError("Min length for contact is 10 and the max is 15")

        return value

