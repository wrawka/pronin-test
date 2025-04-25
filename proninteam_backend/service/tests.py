from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.cache import caches
from service.models import Collection, Payment
from unittest.mock import patch

User = get_user_model()


class SignalTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser")
        self.collection = Collection.objects.create(
            author=self.user,
            name="Test Collection",
            description="A test collection",
            cause=Collection.Cause.WD,
            target_amount=1000.00,
        )

    @patch("service.tasks.send_collection_created_email.delay")
    def test_collection_created_email_signal(self, mock_send_email):
        Collection.objects.create(
            author=self.user,
            name="Another Collection",
            description="Another test collection",
            cause="WD",
            target_amount=2000.00,
        )
        mock_send_email.assert_called_once()

    @patch("service.tasks.send_payment_created_email.delay")
    def test_payment_created_email_signal(self, mock_send_email):
        Payment.objects.create(user=self.user, amount=100.00, collection=self.collection)
        mock_send_email.assert_called_once()

    def test_cache_invalidation_on_collection_save(self):
        cache = caches["api"]
        cache.set("test_key", "test_value")
        self.assertEqual(cache.get("test_key"), "test_value")
        self.collection.save()
        self.assertIsNone(cache.get("test_key"))

    def test_cache_invalidation_on_payment_save(self):
        cache = caches["api"]
        cache.set("test_key", "test_value")
        self.assertEqual(cache.get("test_key"), "test_value")
        Payment.objects.create(user=self.user, amount=100.00, collection=self.collection)
        self.assertIsNone(cache.get("test_key"))
