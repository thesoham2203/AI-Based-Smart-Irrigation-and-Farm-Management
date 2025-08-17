from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime


class ReadingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_reading(self):
        resp = self.client.post("/api/readings/", {
            "timestamp": datetime.utcnow().isoformat(),
            "field_id": "test-field",
            "moisture": 20.5,
        }, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("action", resp.data)
