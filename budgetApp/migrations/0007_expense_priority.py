# Generated by Django 4.1.7 on 2023-04-15 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgetApp', '0006_expense_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='priority',
            field=models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1),
        ),
    ]