from django.shortcuts import render
from rest_framework import generics
from .models import User, Menu, Booking
from .serializers import UserSerializer, MenuSerializer, BookingSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView


########################### PERMISSION CLASSES #####################
class IsChef(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.role == 'chef'
    
class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'

############################ USER VIEWS #####################################   
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginView(TokenObtainPairView):
    pass  

############################## MENU VIEWS ################################

class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsChef]

    def get_queryset(self):
        return Menu.objects.filter(chef__country=self.request.user.country)

    def perform_create(self, serializer):
        print(f"Request user: {self.request.user}")
        serializer.save(chef=self.request.user)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, IsChef]


############################## BOOKING VIEWS ################################
class BookingListCreateView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        menu = serializer.validated_data['menu']
        if menu.chef.country != self.request.user.country:
            raise serializer.ValidationError("Cannot book a menu from a different country.")
        serializer.save(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsUser]