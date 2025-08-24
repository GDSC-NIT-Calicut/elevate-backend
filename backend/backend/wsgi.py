"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()


# --- Auto-create superuser on deploy ---
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()

    
    email = "admin@gmail.com"
    password = "admin"

    if email and password and not User.objects.filter(email=email).exists():
        User.objects.create_superuser( email=email, name="admin", password=password)
        print(f"Superuser '{email}' created.")
except Exception as e:
    # Avoid breaking app if DB isn't ready
    print(f"Superuser creation skipped: {e}")