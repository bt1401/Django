# Generated by Django 3.2.6 on 2021-10-10 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_alter_artical_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artical',
            name='url',
        ),
        migrations.AlterField(
            model_name='artical',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]