# Generated by Django 4.2.2 on 2023-12-18 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_question_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='level',
            field=models.IntegerField(default=0),
        ),
    ]