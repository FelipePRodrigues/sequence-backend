import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from sequence.urls import urlpatterns


class SequenceTest(APITestCase, URLPatternsTestCase):
    urlpatterns = urlpatterns
    databases = {'default'}

    def setUp(self):
        super(SequenceTest, self).setUp()

    def test_no_sequence(self):
        EXPECTED_RESPONSE = "This field is required."
        response = self.client.post(
            reverse("sequence_base:sequence"), data={}, format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)

    def test_empty_sequence(self):
        EXPECTED_RESPONSE = "This field must not be an empty array."
        response = self.client.post(
            reverse("sequence_base:sequence"), data={"letters": []}, format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)

    def test_no_square_sequence(self):
        EXPECTED_RESPONSE = "This field must represent at least a 4x4 square matrix."
        response = self.client.post(reverse("sequence_base:sequence"),
                                    data={"letters": ["BBBB", "BBBB", "BBBB"]},
                                    format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)

    def test_no_minimum_sequence(self):
        EXPECTED_RESPONSE = "This field must represent a square matrix, with at least 4 rows and columns."
        response = self.client.post(reverse("sequence_base:sequence"),
                                    data={"letters": ["BBB", "BBB", "BBB"]},
                                    format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)

    def test_no_string_sequence(self):
        EXPECTED_RESPONSE = "This field must be an array of strings."
        response = self.client.post(reverse("sequence_base:sequence"),
                                    data={"letters": [
                                        "BBBB", "BBBB", "BBBB", 1234]},
                                    format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)

    def test_invalid_letters_sequence(self):
        EXPECTED_RESPONSE = "This field contains invalid letters."
        response = self.client.post(reverse("sequence_base:sequence"),
                                    data={"letters": [
                                        "BBBB", "BBBB", "BBBB", "ZZZZ"]},
                                    format="json")
        content = json.loads(response.content.decode("utf-8")).get("letters")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content[0], EXPECTED_RESPONSE)
