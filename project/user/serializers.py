from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

CustomUser = get_user_model()


User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(max_length=100, required=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email', 'referral_code')
        extra_kwargs = {'email': {'required': False, 'allow_null': True, 'allow_blank': True}}

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', None)
        )
        if referral_code:
            try:
                referrer = User.objects.get(referral=referral_code)
                referrer.friends.append(user.id)
                user.friends.append(referrer.id)
                referrer.save()
                user.save()
            except User.DoesNotExist:
                pass  # Ignore if the referral code is invalid
        return user
    
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
