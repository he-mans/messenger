# Generated by Django 2.1.5 on 2019-03-23 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatsDB', '0002_auto_20190323_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='unread_messages',
            field=models.PositiveIntegerField(default=0),
        ),
    ]