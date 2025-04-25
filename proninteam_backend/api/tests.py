from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from service.models import Collection, Payment

User = get_user_model()


class CollectionAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.collection = Collection.objects.create(
            author=self.user,
            name="Test Collection",
            description="A test collection",
            cause=Collection.Causes.WEDDING,
            target_amount=1000.00,
        )

    def test_list_collections(self):
        response = self.client.get("/api/collections/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Test Collection")

    def test_create_collection(self):
        data = {
            "name": "New Collection",
            "description": "A new test collection",
            "cause": "WD",
            "target_amount": 2000.00,
        }
        response = self.client.post("/api/collections/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Collection")
        self.assertEqual(response.data["author"], self.user.id)

    def test_retrieve_collection(self):
        response = self.client.get(f"/api/collections/{self.collection.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test Collection")

    def test_update_collection(self):
        data = {"name": "Updated Collection"}
        response = self.client.patch(f"/api/collections/{self.collection.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.collection.refresh_from_db()
        self.assertEqual(self.collection.name, "Updated Collection")

    def test_delete_collection(self):
        response = self.client.delete(f"/api/collections/{self.collection.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Collection.objects.filter(id=self.collection.id).exists())


class PaymentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.collection = Collection.objects.create(
            author=self.user,
            name="Test Collection",
            description="A test collection",
            cause=Collection.Causes.BIRTHDAY,
            target_amount=1000.00,
        )

    def test_create_payment(self):
        data = {"amount": 100.00, "collection": self.collection.id, "is_hidden": False}
        response = self.client.post("/api/payments/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["collection"], self.collection.id)

    def test_list_payments(self):
        Payment.objects.create(user=self.user, amount=100.00, collection=self.collection)
        response = self.client.get("/api/payments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["amount"], "100.00")
