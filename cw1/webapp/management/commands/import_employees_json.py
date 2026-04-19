import json
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from webapp.models import Employee

# Fields we persist from JSON (matches Employee model, excluding auto PK/timestamps).
ALLOWED = {
    "emp_id",
    "first_name",
    "last_name",
    "email",
    "department",
    "position",
    "hire_date",
    "salary",
}


def _coerce_defaults(row: dict) -> dict:
    out = {}
    for key in ALLOWED:
        if key not in row:
            continue
        val = row[key]
        if key == "hire_date" and (val is None or val == ""):
            out[key] = None
        elif key == "salary" and (val is None or val == ""):
            out[key] = None
        elif key == "salary" and val is not None:
            try:
                out[key] = Decimal(str(val))
            except (InvalidOperation, TypeError, ValueError) as exc:
                raise ValueError(f"Invalid salary for emp_id={row.get('emp_id')}: {val!r}") from exc
        elif key in ("department", "position") and val is None:
            out[key] = ""
        else:
            out[key] = val

    if "emp_id" not in out:
        raise ValueError("Missing emp_id")
    try:
        out["emp_id"] = int(out["emp_id"])
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid emp_id: {row.get('emp_id')!r}") from exc

    for req in ("first_name", "last_name", "email"):
        if req not in out or str(out[req]).strip() == "":
            raise ValueError(f"emp_id={out.get('emp_id')}: missing required field {req!r}")
    return out


class Command(BaseCommand):
    help = (
        "Import employees from a JSON array (e.g. employees.json). "
        "Ignores id, created_at, updated_at — Django manages primary key and timestamps."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--json",
            dest="json_path",
            type=str,
            default=str(Path(settings.BASE_DIR) / "employees.json"),
            help="Path to JSON file (default: project root employees.json)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and count rows without writing to the database.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete ALL employees before importing (use with --yes).",
        )
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Confirm destructive operations such as --clear.",
        )

    def handle(self, *args, **options):
        path = Path(options["json_path"]).expanduser().resolve()
        dry_run = options["dry_run"]
        clear = options["clear"]
        yes = options["yes"]

        if clear and not yes:
            raise CommandError("Refusing to --clear without --yes (this deletes every employee row).")

        if not path.is_file():
            raise CommandError(f"JSON file not found: {path}")

        with path.open(encoding="utf-8") as handle:
            data = json.load(handle)

        if not isinstance(data, list):
            raise CommandError("JSON root must be an array of employee objects.")

        if clear and not dry_run:
            deleted_count, _details = Employee.objects.all().delete()
            self.stdout.write(
                self.style.WARNING(f"Cleared existing employees ({deleted_count} deletions).")
            )

        created = 0
        updated = 0
        errors = 0

        for idx, row in enumerate(data):
            if not isinstance(row, dict):
                self.stderr.write(self.style.ERROR(f"Row {idx}: expected object, got {type(row).__name__}"))
                errors += 1
                continue
            try:
                defaults = _coerce_defaults(row)
            except ValueError as exc:
                self.stderr.write(self.style.ERROR(f"Row {idx}: {exc}"))
                errors += 1
                continue

            raw_export = row.get("id")
            if raw_export is not None and str(raw_export).strip() != "":
                try:
                    defaults["export_id"] = int(str(raw_export).strip())
                except ValueError:
                    self.stderr.write(
                        self.style.ERROR(f"Row {idx}: invalid JSON id: {raw_export!r}")
                    )
                    errors += 1
                    continue

            emp_id = defaults["emp_id"]
            if dry_run:
                continue

            _, was_created = Employee.objects.update_or_create(
                emp_id=emp_id,
                defaults=defaults,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            f"Loaded {len(data)} objects from {path} (dry_run={dry_run}, errors={errors})"
        )

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run: no database changes were made."))
            return

        self.stdout.write(
            self.style.SUCCESS(f"Created: {created}, updated: {updated}, skipped errors: {errors}")
        )
