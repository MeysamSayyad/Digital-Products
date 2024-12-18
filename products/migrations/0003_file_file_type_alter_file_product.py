# Generated by Django 5.1.3 on 2024-11-30 18:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_category_options_alter_file_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="file_type",
            field=models.PositiveSmallIntegerField(
                choices=[(1, "audio"), (1, "video"), (1, "pdf")],
                default=2,
                verbose_name="file type",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="file",
            name="product",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="files",
                to="products.product",
                verbose_name="product",
            ),
        ),
    ]
