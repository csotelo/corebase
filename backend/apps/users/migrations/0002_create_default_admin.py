import os
from django.db import migrations


def create_default_admin(apps, schema_editor):
    User = apps.get_model("users", "CustomUser")
    email = os.environ.get("DEFAULT_ADMIN_EMAIL", "admin@corebase.local")
    password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "P4ssw0rd!")
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            email=email,
            password=password,
            is_email_verified=True,
        )


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_admin, migrations.RunPython.noop),
    ]
