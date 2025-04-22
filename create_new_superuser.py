import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mypage.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create a new superuser with simple credentials
username = 'berserk'
email = 'berserk@example.com'
password = 'berserk123'

try:
    user = User.objects.create_superuser(username, email, password)
    print(f"Superuser created successfully!")
    print(f"Username: {username}")
    print(f"Email: {email}")
    print(f"Password: {password}")
except Exception as e:
    print(f"Error creating superuser: {e}")
