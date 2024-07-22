from rest_framework import serializers
from ..models import Account
from users.models import CustomUser as User

class AccountUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'password', 'username', 'email', 'name')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class AccountSerializer(serializers.ModelSerializer):
    user = AccountUserSerializer()
    
    class Meta:
        model = Account
        fields = '__all__'
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = AccountUserSerializer().create(user_data)
        account = Account.objects.create(user=user, **validated_data)
        return account
