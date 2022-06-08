from rest_framework import serializers

from accounts.models import MyUser


class MyUserSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = MyUser
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }
    
    def create(self, validate_data):
        return MyUser.objects.create_user(**validate_data)
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords does'nt match")
        return attrs


class MyUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = MyUser
        fields = '__all__'
