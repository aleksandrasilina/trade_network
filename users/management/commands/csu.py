from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """Команда для создания суперпользователя."""

    def handle(self, *args, **options):
        user = User.objects.create(email="admin@email.com")
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.set_password("123456")
        user.save()
