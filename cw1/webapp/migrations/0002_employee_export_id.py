from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("webapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="employee",
            name="export_id",
            field=models.PositiveIntegerField(
                blank=True,
                db_index=True,
                null=True,
                unique=True,
                help_text="Optional sequence id from JSON export (original `id` field).",
            ),
        ),
    ]
