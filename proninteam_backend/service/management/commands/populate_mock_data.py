import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from service.models import Collection, Payment

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Заполнение базы данных тестовыми данными"

    def handle(self, *args, **kwargs):
        self.stdout.write("Создание тестовых данных...")
        if Collection.objects.exists() or Payment.objects.exists():
            self.stdout.write(self.style.WARNING("В базе уже что-то есть, давайте не будем трогать. 🤔"))
            return

        # Создание 10 пользователей
        users = []
        for _ in range(10):
            user = User.objects.create_user(
                username=fake.user_name(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                password="password123",
            )
            users.append(user)
        self.stdout.write("Создано 10 пользователей.")

        # Создание 10 сборов
        collections = []
        for _ in range(random.randint(50, 100)):
            collection = Collection.objects.create(
                author=random.choice(users),
                name=fake.sentence(nb_words=3),
                description=fake.text(),
                cause=random.choice([choice[0] for choice in Collection.Causes.choices]),
                target_amount=random.randint(1000, 50000),
                cover_image=fake.image_url(),
                due_date=fake.future_datetime(),
            )
            collections.append(collection)
        self.stdout.write("Создано 10 сборов.")

        # Создание 10-100 платежей для каждого сбора
        for collection in collections:
            num_payments = random.randint(10, 100)
            for _ in range(num_payments):
                Payment.objects.create(
                    user=random.choice(users),
                    amount=random.uniform(10, 500),
                    collection=collection,
                    is_hidden=random.choice([True, False]),
                )
        self.stdout.write("Созданы платежи для каждого сбора.")

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
