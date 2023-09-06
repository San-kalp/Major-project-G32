# Generated by Django 4.2.3 on 2023-08-08 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="fraudlent_data_tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(max_length=30)),
                ("exposure", models.CharField(max_length=30)),
                ("cluster_label", models.IntegerField()),
                ("predicted_cluster_label", models.IntegerField()),
                ("sanction_label", models.CharField(max_length=30)),
            ],
        ),
    ]
