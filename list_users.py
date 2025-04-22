import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypage.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# List all users
users = User.objects.all()
print("Existing users:")
for user in users:
    print(f"Username: {user.username}, Email: {user.email}, Is superuser: {user.is_superuser}")
