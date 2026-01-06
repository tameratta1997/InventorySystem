import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User

username = os.environ.get("ADMIN_USER", "admin")
email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
password = os.environ.get("ADMIN_PASSWORD", "admin12345")

if not User.objects.filter(username=username).exists():
    print(f"Creating superuser {username}...")
    User.objects.create_superuser(username, email, password)
    print("Superuser created successfully!")
else:
    print(f"Superuser {username} already exists.")
