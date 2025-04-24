from celery import shared_task
from django.core.mail import send_mail
from service.models import Collection, Payment


@shared_task
def send_collection_created_email(collection_id):
    """Отправить уведомление автору о созданном сборе."""
    try:
        collection = Collection.objects.get(id=collection_id)
        subject = f"Создан новый сбор: {collection.name}"
        message = (
            f"Уважаемый(-ая) {collection.author.username},\n\n"
            f"Ваш сбор '{collection.name}' был успешно создан.\n\n"
            f"Подробнее:\n"
            f"Повод: {collection.get_cause_display()}\n"
            f"Целевая сумма: {collection.target_amount}\n"
            f"Описание: {collection.description}"
        )
        send_mail(subject, message, "no-reply@example.com", [collection.author.email])
    except Collection.DoesNotExist:
        pass


@shared_task
def send_payment_created_email(payment_id):
    """Отправить уведомление об успешном платеже."""
    try:
        payment = Payment.objects.get(id=payment_id)
        subject = f"Получен платёж для: {payment.collection.name}"
        message = (
            f"Уважаемый(-ая) {payment.user.username},\n\n"
            f"Вы задонатили {payment.amount} на сбор '{payment.collection.name}'."
        )
        send_mail(subject, message, "no-reply@example.com", [payment.user.email])
    except Payment.DoesNotExist:
        pass
