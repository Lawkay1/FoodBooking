from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User



class UserTests(APITestCase):
    def test_user_registration(self):
        url = reverse('register')
        data = {
            'username': 'testuuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'role': 'user',
            'country': 'NG'
        }
        response = self.client.post(url, data, format='json')
        print(response.data, 'registration')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def setUp(self):
        # Create an active user for testing
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            is_active=True  # Ensure the user is active
        )

    def test_user_login(self):
        #self.test_user_registration()  # Register user first
        url = reverse('login')
        data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        print('login', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)  # Ensure JWT token is returned

    def tearDown(self):
        
        User.objects.all().delete()
from .models import Menu, Booking

class MenuTests(APITestCase):
    def setUp(self):
        self.chef = User.objects.create_user(username='chefuser', password='testpassword123', role='chef', country='NG')

        # Perform login
        url = reverse('login')
        login_data = {
            'username': 'chefuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']

        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_menu(self):
        url = reverse('menu-list-create')
        data = {
            'name': 'Sample Menu',
            'description': 'Delicious food',
            'price': '50.00',
            'chef': self.chef.id
        }
        response = self.client.post(url, data, format='json')
        
        print(response.data)  # Check response if there are errors
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().name, 'Sample Menu')
    # ... (other test methods)

class BookingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='regularuser', password='testpassword123', role='user', country='NG')
        self.chef = User.objects.create_user(username='chefuser', password='testpassword123', role='chef', country='NG')

        # Perform login for user
        url = reverse('login')
        login_data = {
            'username': 'regularuser',
            'password': 'testpassword123'
        }
        response = self.client.post(url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']

        # Set authorization header
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.menu = Menu.objects.create(name='Sample Menu', description='Delicious food', price='50.00', chef=self.chef)

    def test_create_booking(self):
        url = reverse('booking-list-create')
        data = {
            'menu': self.menu.id,
            'booking_date': '2024-08-10T14:00:00Z',
            'venue': 'Test Venue',
            'guests': 10,
            'user': self.user.id
        }
        response = self.client.post(url, data, format='json')
        print(response.data, 'response.data')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
    
    def test_booking_country_restriction(self):
        self.client.logout()

        # Perform login for a user in a different country
        self.user_gh = User.objects.create_user(username='ghuser', password='testpassword123', role='user', country='GH')
        login_data = {
            'username': 'ghuser',
            'password': 'testpassword123'
        }
        response = self.client.post(reverse('login'), login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        url = reverse('booking-list-create')
        data = {
            'menu': self.menu.id,
            'booking_date': '2024-08-10T14:00:00Z',
            'venue': 'Test Venue',
            'guests': 10
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Booking.objects.count(), 0)  # Booking should not be allowed for a different country's menu
