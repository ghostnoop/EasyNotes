# Generated by Django 3.0.5 on 2020-07-18 18:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0005_noteboard_pub_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noteboard',
            name='note_text',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]