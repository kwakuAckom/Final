# Generated by Django 4.1.7 on 2023-04-22 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0013_alter_project_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.TextField(max_length=30),
        ),
    ]
