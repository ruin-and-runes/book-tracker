from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [

        migrations.AddField(
            model_name='book',
            name='times_read',
            field=models.IntegerField(default=0),
        ),

        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(max_length=20, default='read'),
        ),

        migrations.AddField(
            model_name='book',
            name='progress',
            field=models.IntegerField(default=0),
        ),

        migrations.AddField(
            model_name='book',
            name='cover_url',
            field=models.URLField(blank=True, null=True),
        ),

        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(upload_to='covers/', blank=True, null=True),
        ),

        migrations.AddField(
            model_name='book',
            name='is_comfort',
            field=models.BooleanField(default=False),
        ),

        migrations.AddField(
            model_name='book',
            name='release_date',
            field=models.DateField(blank=True, null=True),
        ),

        migrations.AddField(
            model_name='book',
            name='is_released',
            field=models.BooleanField(default=True),
        ),
    ]
