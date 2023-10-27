# Generated by Django 4.1.2 on 2022-11-16 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0009_rename_input_time_personalfinance_update_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('expense_type', models.CharField(max_length=1)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('effective_time', models.DateTimeField(auto_now_add=True)),
                ('finances', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mainapp.personalfinance')),
            ],
        ),
    ]
