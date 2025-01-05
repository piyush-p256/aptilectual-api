# Generated by Django 5.0.7 on 2025-01-05 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aptitude', '0006_customuser_daily_top_positions_useranswer_is_correct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='daily_top_positions',
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_position_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='second_position_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='third_position_count',
            field=models.IntegerField(default=0),
        ),
    ]
