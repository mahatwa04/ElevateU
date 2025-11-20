from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # This migration has been emptied as the model operations reference
        # models that belong to other apps (users, posts, engagement)
        # and are causing a KeyError during migration execution.
        # Each app should have its own migrations for its models.
    ]
