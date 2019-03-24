# Generated by Django 2.1.7 on 2019-03-24 03:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0003_auto_20190324_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(verbose_name=datetime.datetime(2019, 3, 24, 3, 20, 6, 120492, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='groupmembers',
            name='category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='Groups.ExpenseCategory'),
        ),
    ]