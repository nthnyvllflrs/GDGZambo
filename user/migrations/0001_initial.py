# Generated by Django 2.1.4 on 2019-02-21 23:47

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('become_a_sponsor_url', models.URLField(default='https://gdgzamboanga.herokuapp.com/', max_length=1000)),
                ('become_a_volunteer_url', models.URLField(default='https://gdgzamboanga.herokuapp.com/', max_length=1000)),
                ('speaker_request_url', models.URLField(default='https://gdgzamboanga.herokuapp.com/', max_length=1000)),
                ('media_kit_url', models.URLField(default='https://gdgzamboanga.herokuapp.com/', max_length=1000)),
                ('photo_gallery_url', models.URLField(default='https://gdgzamboanga.herokuapp.com/', max_length=1000)),
                ('about_us', models.TextField(default='GDG Zamboanga')),
                ('google_plus_link', models.URLField(default='https://plus.google.com/', max_length=300)),
                ('facebook_link', models.URLField(default='https://facebook.com/', max_length=300)),
                ('twitter_link', models.URLField(default='https://twitter.com', max_length=300)),
                ('youtube_link', models.URLField(default='https://youtube.com', max_length=300)),
                ('instagram_link', models.URLField(default='https://instagram.com', max_length=300)),
                ('meetup_link', models.URLField(default='https://meetup.com', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='SiteCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(default='Blog Creator', max_length=120)),
                ('activated', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='team.Member')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
