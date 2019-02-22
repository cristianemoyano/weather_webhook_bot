# Generated by Django 2.1.7 on 2019-02-22 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('access_token', models.TextField()),
                ('category', models.CharField(blank=True, max_length=250, null=True)),
                ('page_name', models.CharField(blank=True, max_length=250, null=True)),
                ('page_id', models.CharField(blank=True, max_length=250, null=True)),
                ('page_tasks', models.TextField()),
                ('default', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
