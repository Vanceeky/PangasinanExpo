# Generated by Django 5.0.4 on 2024-11-19 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_tourist_avatar_testimonial_testimonialimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]