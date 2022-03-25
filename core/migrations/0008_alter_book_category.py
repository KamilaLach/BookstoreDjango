# Generated by Django 4.0.3 on 2022-03-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_book_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('Education', 'Education'), ('Comics', 'Comics'), ('Biography', 'Biography'), ('History', 'History'), ('Novel', 'Novel'), ('Fantasy', 'Fantasy'), ('Thriller', 'Thriller'), ('Romance', 'Romance'), ('Sci-Fi', 'Sci-Fi')], default='Education', max_length=30),
        ),
    ]
