import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from sequence.urls import urlpatterns


class SequenceTest(APITestCase, URLPatternsTestCase):
    urlpatterns = urlpatterns
    databases = {"default"}

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
        EXPECTED_RESPONSE = "This field must represent a square matrix, with at least 4 rows and columns."
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

    def test_valid_sequence(self):
        with self.subTest():
            sequence = [
                "BBDU",
                "BHDH",
                "BBDU",
                "BHDH",
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, True)

        with self.subTest():
            sequence = [
                "BDDU",
                "DBUD",
                "DUBD",
                "UDDB",
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, True)

        with self.subTest():
            sequence = [
                "BBBB",
                "UHUH",
                "DDDD",
                "UHUH",
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, True)

        with self.subTest():
            sequence = [
                "BBUUBB",
                "DDHHBD",
                "BBUBBB",
                "DDBHDD",
                "BBUUBB",
                "DDHHDD"
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, True)

    def test_invalid_sequence(self):
        with self.subTest():
            sequence = [
                "BBBB",
                "UHUH",
                "UHUH",
                "UHUH",
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, False)

        with self.subTest():
            sequence = [
                "BBBBD",
                "UHUHD",
                "UHUHH",
                "UHUHD",
                "BDBBD",
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, False)

        with self.subTest():
            sequence = [
                "BBUUBB",
                "DDHHBD",
                "BBUBBB",
                "DDBHDD",
                "BDUUBB",
                "DDHHDD"
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, False)

        with self.subTest():
            sequence = [
                "BBBU",
                "BDHH",
                "BBUB",
                "BDBH"
            ]
            response = self.client.post(reverse("sequence_base:sequence"),
                                        data={"letters": sequence},
                                        format="json")
            content = json.loads(
                response.content.decode("utf-8")).get("is_valid")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(content, False)
