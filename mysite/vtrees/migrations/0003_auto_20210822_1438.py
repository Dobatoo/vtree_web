# Generated by Django 3.2.6 on 2021-08-22 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vtrees', '0002_alter_videos_videos_lastupdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channels_info',
            fields=[
                ('channels_id', models.SlugField(max_length=24, primary_key=True, serialize=False)),
                ('channels_title', models.CharField(max_length=100)),
                ('channels_count_total', models.BigIntegerField(default=0)),
                ('channels_icon_url', models.URLField()),
                ('channels_isRegistered', models.BooleanField(default=False)),
                ('channels_info_lastupdate', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Children',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Mentions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mentions_channel_id', models.SlugField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Videos_info',
            fields=[
                ('videos_id', models.SlugField(max_length=11, primary_key=True, serialize=False)),
                ('videos_title', models.CharField(max_length=100)),
                ('videos_published', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Videos',
        ),
        migrations.CreateModel(
            name='Channels_detail',
            fields=[
                ('channels_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vtrees.channels_info')),
                ('channels_count_sited_sum', models.BigIntegerField(default=0)),
                ('channels_count_sited_sum_lastupdate', models.DateTimeField(blank=True, null=True)),
                ('channels_count_mentioned_sum', models.BigIntegerField(default=0)),
                ('channels_count_mentioned_sum_lastupdate', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('posts_video_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vtrees.videos_info')),
                ('posts_channel_id', models.SlugField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='Videos_detail',
            fields=[
                ('videos_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='vtrees.videos_info')),
                ('videos_description', models.TextField(max_length=5000)),
                ('videos_count_original', models.BigIntegerField(default=0)),
                ('videos_detail_lastupdate', models.DateTimeField()),
                ('videos_count_sited', models.BigIntegerField(default=0)),
                ('videos_count_sited_lastupdate', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mentions',
            name='mentions_video_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vtrees.videos_info'),
        ),
        migrations.AddField(
            model_name='children',
            name='children_video_child',
            field=models.ManyToManyField(related_name='child_table', to='vtrees.Videos_info'),
        ),
        migrations.AddField(
            model_name='children',
            name='children_video_parent',
            field=models.ManyToManyField(related_name='parent_table', to='vtrees.Videos_info'),
        ),
    ]
