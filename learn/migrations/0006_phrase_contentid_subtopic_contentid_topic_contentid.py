# Generated by Django 5.2 on 2025-04-18 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learn', '0005_alter_phrase_topic'),
    ]

    operations = [
        migrations.AddField(
            model_name='phrase',
            name='contentID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subtopic',
            name='contentID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='topic',
            name='contentID',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
