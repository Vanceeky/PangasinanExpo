# Generated by Django 5.0.4 on 2024-11-02 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_accomodation_date_created_accomodation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomodation',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
