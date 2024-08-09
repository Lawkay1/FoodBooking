from rest_framework import serializers
from .models import User, Menu, Booking
import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'country', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email'),
            country=validated_data.get('country'),
            role = validated_data.get('role'),
            is_active=True,
        )
        return user


class MenuSerializer(serializers.ModelSerializer):
    chef = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'price', 'chef']
        


    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['chef'] = request.user  
        print(f"Creating menu with chef: {validated_data['chef']}") 
        return super().create(validated_data)

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.PrimaryKeyRelatedField(read_only=True)
        model = Booking
        fields = ['id', 'user', 'menu', 'booking_date', 'venue', 'guests']
        read_only_fields = ['booking_date', 'user']
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user  
        validated_data['booking_date'] = datetime.datetime.now() 
        
        return super().create(validated_data)
