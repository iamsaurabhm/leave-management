# Generated by Django 3.2 on 2022-02-18 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0003_auto_20220218_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='client',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='employee.client'),
        ),
    ]
