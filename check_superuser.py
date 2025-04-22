import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypage.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Check if berserk is a superuser
try:
    user = User.objects.get(username='berserk')
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is staff: {user.is_staff}")
    print(f"Date joined: {user.date_joined}")
except User.DoesNotExist:
    print("User 'berserk' does not exist.")
