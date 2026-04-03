from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='status',
            field=models.CharField(max_length=20, default='read'),
        ),
        migrations.AddField(
            model_name='book',
            name='times_read',
            field=models.IntegerField(default=0),
        ),
    ]