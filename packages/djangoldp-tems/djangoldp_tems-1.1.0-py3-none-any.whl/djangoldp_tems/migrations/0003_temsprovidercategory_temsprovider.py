# Generated by Django 4.2.16 on 2024-11-11 14:01

from django.db import migrations, models
import django.db.models.deletion
import djangoldp.fields


class Migration(migrations.Migration):

    dependencies = [
        ("djangoldp_tems", "0002_alter_temsimages_name_alter_temslicence_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="TEMSProviderCategory",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urlid",
                    djangoldp.fields.LDPUrlField(
                        blank=True, db_index=True, null=True, unique=True
                    ),
                ),
                (
                    "is_backlink",
                    models.BooleanField(
                        default=False,
                        help_text="set automatically to indicate the Model is a backlink",
                    ),
                ),
                (
                    "allow_create_backlink",
                    models.BooleanField(
                        default=True,
                        help_text="set to False to disable backlink creation after Model save",
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=254, null=True),
                ),
            ],
            options={
                "verbose_name": "TEMS Category",
                "verbose_name_plural": "TEMS Categories",
                "abstract": False,
                "default_permissions": {"delete", "control", "add", "change", "view"},
                "rdf_type": "tems:Category",
                "container_path": "/providers/categories/",
                "serializer_fields": ["@id", "creation_date", "update_date", "name"],
                "nested_fields": [],
                "depth": 0,
            },
        ),
        migrations.CreateModel(
            name="TEMSProvider",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "urlid",
                    djangoldp.fields.LDPUrlField(
                        blank=True, db_index=True, null=True, unique=True
                    ),
                ),
                (
                    "is_backlink",
                    models.BooleanField(
                        default=False,
                        help_text="set automatically to indicate the Model is a backlink",
                    ),
                ),
                (
                    "allow_create_backlink",
                    models.BooleanField(
                        default=True,
                        help_text="set to False to disable backlink creation after Model save",
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("description", models.TextField(blank=True, default="", null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="djangoldp_tems.temsprovidercategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "TEMS Provider",
                "verbose_name_plural": "TEMS Providers",
                "abstract": False,
                "default_permissions": {"delete", "control", "add", "change", "view"},
                "rdf_type": "tems:Provider",
                "container_path": "/providers/",
                "serializer_fields": [
                    "@id",
                    "creation_date",
                    "update_date",
                    "name",
                    "description",
                    "category",
                ],
                "nested_fields": ["category"],
                "depth": 0,
            },
        ),
    ]
