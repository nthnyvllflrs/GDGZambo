# Generated by Django 2.1.4 on 2019-03-05 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='member_speaker',
            field=models.ManyToManyField(blank=True, to='team.Member'),
        ),
        migrations.AlterField(
            model_name='event',
            name='member_sponsor',
            field=models.ManyToManyField(blank=True, related_name='sponsored_events', to='team.Member'),
        ),
        migrations.AlterField(
            model_name='event',
            name='member_volunteer',
            field=models.ManyToManyField(blank=True, related_name='volunteered_events', to='team.Member'),
        ),
        migrations.AlterField(
            model_name='event',
            name='volunteers',
            field=models.ManyToManyField(blank=True, to='team.Volunteer'),
        ),
    ]
