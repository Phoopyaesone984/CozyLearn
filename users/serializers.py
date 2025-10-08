from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user registration.
    Requires password confirmation and securely creates the User object.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    token = serializers.SerializerMethodField(read_only=True)  # Field to return the token upon registration

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio', 'profile_pic',
                  'token')
        extra_kwargs = {'email': {'required': True}}

    def get_token(self, user):
        """
        Retrieves or creates a Token for the user.
        """
        token, created = Token.objects.get_or_create(user=user)
        return token.key

    def validate(self, data):
        """Check that the two password fields match."""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        """Create and return a new User instance, hashing the password."""
        # Remove password2 before creation
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            bio=validated_data.get('bio', ''),
            profile_pic=validated_data.get('profile_pic', None),
        )
        # We need to manually create a token so the user can be logged in immediately
        Token.objects.get_or_create(user=user)
        return user


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer used for the login endpoint to authenticate credentials.
    """
    username = serializers.CharField(label=_("Username"))
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    user_id = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Authenticate user using Django's built-in function
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        # Attach the user object for use in the view
        attrs['user'] = user

        # Attach the user ID and Token to the validated data for the response
        attrs['user_id'] = user.id
        token, created = Token.objects.get_or_create(user=user)
        attrs['token'] = token.key

        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user profiles (non-sensitive fields).
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_pic')
        read_only_fields = ('username', 'email')
