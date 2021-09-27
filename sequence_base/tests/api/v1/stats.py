import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from sequence.urls import urlpatterns


class StatsTest(APITestCase, URLPatternsTestCase):
    urlpatterns = urlpatterns
    databases = {"default"}

    def setUp(self):
        super(StatsTest, self).setUp()

    def test_stats(self):
        with self.subTest():
            sequence = ["BBDU", "BHDH", "BBDU", "BHDH"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            sequence = ["BDDU", "DBUD", "DUBD", "UDDB"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            response = self.client.get(
                reverse("sequence_base:stats"), format="json")
            content = json.loads(response.content.decode("utf-8"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content.get("count_valid"), 2)
            self.assertEqual(content.get("count_invalid"), 0)
            self.assertEqual(content.get("ratio"), 1.0)

        with self.subTest():
            sequence = ["BBDU", "BHDH", "DBDU", "BHDH"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            response = self.client.get(
                reverse("sequence_base:stats"), format="json")
            content = json.loads(response.content.decode("utf-8"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content.get("count_valid"), 2)
            self.assertEqual(content.get("count_invalid"), 1)
            self.assertEqual(content.get("ratio"), 0.67)

        with self.subTest():
            sequence = ["BBDD", "HUHU", "BBDD", "HUHU"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            response = self.client.get(
                reverse("sequence_base:stats"), format="json")
            content = json.loads(response.content.decode("utf-8"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content.get("count_valid"), 2)
            self.assertEqual(content.get("count_invalid"), 2)
            self.assertEqual(content.get("ratio"), 0.5)

        with self.subTest():
            sequence = ["DDBB", "UUHH", "UUHH", "DDBB"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            sequence = ["BDDDB", "HUHUH", "HBDDB", "BHUHU", "HUHDB"]
            self.client.post(reverse("sequence_base:sequence"),
                             data={"letters": sequence},
                             format="json")

            response = self.client.get(
                reverse("sequence_base:stats"), format="json")
            content = json.loads(response.content.decode("utf-8"))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content.get("count_valid"), 2)
            self.assertEqual(content.get("count_invalid"), 4)
            self.assertEqual(content.get("ratio"), 0.33)

    def test_invalid_stats(self):
        sequence = ["DDBB", "UUHH", "UUHH", "DDBB"]
        self.client.post(reverse("sequence_base:sequence"),
                         data={"letters": sequence},
                         format="json")

        response = self.client.get(
            reverse("sequence_base:stats"), format="json")
        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("count_valid"), 0)
        self.assertEqual(content.get("count_invalid"), 1)
        self.assertEqual(content.get("ratio"), 0)

    def test_null_stats(self):
        response = self.client.get(
            reverse("sequence_base:stats"), format="json")
        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content.get("count_valid"), 0)
        self.assertEqual(content.get("count_invalid"), 0)
        self.assertEqual(content.get("ratio"), 0)
