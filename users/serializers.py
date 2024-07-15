from common import DynamicFieldsModelSerializer
from .models import CustomUser

class CustomUserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user