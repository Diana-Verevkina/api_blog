# Generated by Django 3.2.20 on 2023-08-09 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0013_alter_post_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(blank=True, help_text='Введите текст поста', max_length=140, null=True, verbose_name='Текст поста'),
        ),
    ]