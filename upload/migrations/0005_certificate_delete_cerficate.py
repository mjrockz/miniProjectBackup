# Generated by Django 4.2.1 on 2023-06-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0004_cerficate_points'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.CharField(max_length=100)),
                ('file', models.ImageField(blank=True, upload_to='media/certificates')),
                ('points', models.IntegerField(default=0)),
            ],
        ),
        migrations.DeleteModel(
            name='Cerficate',
        ),
    ]
