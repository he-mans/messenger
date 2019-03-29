# Generated by Django 2.1.5 on 2019-03-28 07:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chatsDB', '0014_auto_20190325_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='last_message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='chatsDB.Messages'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='unread_messages',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
