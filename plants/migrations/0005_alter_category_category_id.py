# Generated by Django 5.1 on 2024-09-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plants', '0004_alter_category_table_alter_floweringcategory_table_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_id',
            field=models.AutoField(db_column='CategoryID', primary_key=True, serialize=False),
        ),
    ]
