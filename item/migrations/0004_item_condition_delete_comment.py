# Generated by Django 4.2.11 on 2024-03-27 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0003_review_review_desp'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='condition',
            field=models.CharField(choices=[('NEW', 'New'), ('USED', 'Second Hand/Used')], default='NEW', max_length=4),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
