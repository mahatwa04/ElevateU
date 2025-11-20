from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Add indexes for frequently queried fields
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='campus_email',
            field=models.EmailField(db_index=True, unique=True),
        ),
        migrations.AddIndex(
            model_name='customuser',
            index=models.Index(fields=['created_at'], name='core_customuser_created_at_idx'),
        ),
        # Post indexes
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['user', 'created_at'], name='core_post_user_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['category', '-created_at'], name='core_post_category_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['created_at'], name='core_post_created_at_idx'),
        ),
        # Achievement indexes
        migrations.AddIndex(
            model_name='achievement',
            index=models.Index(fields=['author', 'category'], name='core_achievement_author_category_idx'),
        ),
        migrations.AddIndex(
            model_name='achievement',
            index=models.Index(fields=['category', '-created_at'], name='core_achievement_category_created_idx'),
        ),
    ]
