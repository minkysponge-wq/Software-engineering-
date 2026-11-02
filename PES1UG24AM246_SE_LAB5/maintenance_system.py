"""Warehouse asset maintenance registry.

Registers machines, records service dates, raises alerts for overdue
inspections and exports a report to ``maintenance.json``.
"""

import json
import tempfile
from datetime import datetime, timedelta

DATE_FORMAT = "%Y-%m-%d"

# Global state
assets = {}
registration_log = []
settings = {"service_interval_days": 90}


def register_asset(asset_id, machine_type, logs=None):
    """Register an asset; reject empty or duplicate IDs."""
    if logs is None:
        logs = registration_log
    if not asset_id or not asset_id.strip():
        print("Rejected: asset ID must not be empty")
        return False
    if asset_id in assets:
        print("Rejected:", asset_id, "is already registered as",
              assets[asset_id]["type"])
        return False
    assets[asset_id] = {
        "type": machine_type,
        "last_service": datetime.now().strftime(DATE_FORMAT),
    }
    logs.append(asset_id)
    print("Registered", asset_id,
          "- total registrations this run:", len(logs))
    return True


def update_service_date(asset_id, date):
    """Set the last service date (YYYY-MM-DD, not in the future)."""
    try:
        parsed = datetime.strptime(date, DATE_FORMAT)
    except ValueError:
        print("Invalid date", repr(date), "- expected YYYY-MM-DD")
        return False
    if parsed > datetime.now():
        print("Rejected: service date", date, "is in the future")
        return False
    try:
        assets[asset_id]["last_service"] = date
    except KeyError:
        print("Could not update", asset_id, "- unknown asset")
        return False
    return True


def due_for_inspection():
    """Return IDs of assets whose last service exceeds the interval."""
    interval = timedelta(days=settings["service_interval_days"])
    due = []
    for asset_id, info in assets.items():
        last = datetime.strptime(info["last_service"], DATE_FORMAT)
        if datetime.now() - last > interval:
            due.append(asset_id)
    return due


def change_interval(days):
    """Change the service interval; must be a positive whole number."""
    if not isinstance(days, int) or days <= 0:
        print("Rejected: service interval must be a positive integer,",
              "keeping", settings["service_interval_days"], "days")
        return False
    settings["service_interval_days"] = days
    return True


def export_service_report(filename="maintenance.json"):
    """Write all assets to a JSON report file."""
    with open(filename, "w", encoding="utf-8") as report:
        json.dump(assets, report, indent=2)
    print("Report written to " + filename)


def write_scratch_copy():
    """Write a scratch copy of the registry to a secure temp file."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as scratch:
        json.dump(assets, scratch)
    print("Scratch copy at", scratch.name)


def print_alerts():
    """Print an alert for every asset that is overdue for inspection."""
    for asset_id in due_for_inspection():
        print("ALERT: inspection overdue for", asset_id,
              assets[asset_id]["type"])


def main():
    """Run the demo workflow."""
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(-30)
    date = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if date:
        update_service_date("CV-07", date.strip())
    if not assets:
        print("No assets registered; nothing to report")
        return
    print_alerts()
    export_service_report()
    write_scratch_copy()


if __name__ == "__main__":
    main()
