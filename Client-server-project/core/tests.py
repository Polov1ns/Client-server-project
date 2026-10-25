from core.models import Resource, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ResourceAndBookingAPITests(APITestCase):

  def setUp(self):
    # Тестовий користувач і ресурс
    self.user = User.objects.create_user(
        username='testclient', password='password123'
    )
    self.resource_data = {
        'name': 'Test Room',
        'resource_type': 'Conference Room',
        'description': 'A room for testing',
        'price_per_hour': '150.00',
    }
    self.resource = Resource.objects.create(**self.resource_data)
    self.resources_url = reverse('resource-list')

  def test_get_resources_list_returns_200(self):
    """Інтеграційний тест: перевірка отримання списку ресурсів (код 200)"""
    response = self.client.get(self.resources_url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertGreaterEqual(response.data['count'], 1)

  def test_create_resource_with_valid_data_returns_201(self):
    """Інтеграційний тест: створення нового ресурсу повертає 201 Created"""
    payload = {
        'name': 'New Office',
        'resource_type': 'Workplace',
        'description': 'Desks and computers',
        'price_per_hour': '300.00',
    }
    response = self.client.post(self.resources_url, payload, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Resource.objects.count(), 2)

  def test_create_resource_with_invalid_data_returns_400(self):
    """Інтеграційний тест: некоректні дані повертають 400 Bad Request"""
    payload = {
        'name': '',  #Порожне ымя викличе помилку
        'resource_type': 'Workplace',
        'price_per_hour': '300.00',
    }
    response = self.client.post(self.resources_url, payload, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)