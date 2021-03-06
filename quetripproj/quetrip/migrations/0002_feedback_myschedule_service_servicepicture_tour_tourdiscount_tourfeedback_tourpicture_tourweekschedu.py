# Generated by Django 2.2.7 on 2019-12-02 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quetrip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=11)),
                ('member_name', models.CharField(max_length=50)),
                ('member_picture', models.CharField(max_length=1000)),
                ('ratings', models.CharField(max_length=11)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MySchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member_id', models.CharField(max_length=11)),
                ('tour_id', models.CharField(max_length=11)),
                ('subject', models.CharField(max_length=100)),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
                ('picture_url', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('status', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manager_id', models.CharField(max_length=11)),
                ('category', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('subcategory', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('postal', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('picture_url', models.CharField(max_length=1000)),
                ('video_url', models.CharField(max_length=1000)),
                ('price', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2000)),
                ('since', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ServicePicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=11)),
                ('picture_url', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Tour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_id', models.CharField(max_length=11)),
                ('name', models.CharField(max_length=200)),
                ('phone_number', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('postal', models.CharField(max_length=100)),
                ('latitude', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('picture_url', models.CharField(max_length=1000)),
                ('video_url', models.CharField(max_length=1000)),
                ('price', models.CharField(max_length=50)),
                ('discount', models.CharField(max_length=30)),
                ('language', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=2000)),
                ('highlights', models.CharField(max_length=1000)),
                ('policy', models.CharField(max_length=1000)),
                ('ratings', models.CharField(max_length=11)),
                ('reviews', models.CharField(max_length=11)),
                ('since', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TourDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_id', models.CharField(max_length=11)),
                ('discount', models.CharField(max_length=11)),
            ],
        ),
        migrations.CreateModel(
            name='TourFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_id', models.CharField(max_length=11)),
                ('member_id', models.CharField(max_length=11)),
                ('member_name', models.CharField(max_length=50)),
                ('member_picture', models.CharField(max_length=1000)),
                ('ratings', models.CharField(max_length=11)),
                ('subject', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=2000)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TourPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_id', models.CharField(max_length=11)),
                ('picture_url', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TourWeekSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tour_id', models.CharField(max_length=11)),
                ('week_name', models.CharField(max_length=30)),
                ('open_time', models.CharField(max_length=50)),
                ('adults', models.CharField(max_length=11)),
                ('seniors', models.CharField(max_length=11)),
                ('children', models.CharField(max_length=11)),
                ('infants', models.CharField(max_length=11)),
                ('tourists', models.CharField(max_length=11)),
                ('status', models.CharField(max_length=30)),
            ],
        ),
    ]
