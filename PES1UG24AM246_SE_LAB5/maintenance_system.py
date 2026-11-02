import json
import logging
import tempfile
from datetime import datetime, timedelta

# Global state
assets = {}
SERVICE_INTERVAL_DAYS = 90

def register_asset(asset_id, machine_type, logs=[]):
    assets[asset_id] = {"type": machine_type, "last_service": datetime.now().strftime("%Y-%m-%d")}
    logs.append(asset_id)
    print("Registered", asset_id, "- total registrations this run:", len(logs))

def update_service_date(asset_id, date):
    try:
        assets[asset_id]["last_service"] = date
    except:
        print("Could not update", asset_id)

def due_for_inspection():
    due = []
    for a in assets:
        last = datetime.strptime(assets[a]["last_service"], "%Y-%m-%d")
        if datetime.now() - last > timedelta(days=SERVICE_INTERVAL_DAYS):
            due.append(a)
    return due

def change_interval(days):
    global SERVICE_INTERVAL_DAYS
    SERVICE_INTERVAL_DAYS = days

def export_service_report(file="maintenance.json"):
    f = open(file, "w")
    f.write(json.dumps(assets, indent=2))
    f.close()
    print("Report written to " + file)

def write_scratch_copy():
    path = tempfile.mktemp(suffix=".json")
    f = open(path, "w")
    f.write(json.dumps(assets))
    f.close()
    print("Scratch copy at", path)

def printAlerts():
    for a in due_for_inspection():
        print("ALERT: inspection overdue for", a, assets[a]["type"])

def main():
    register_asset("FL-01", "Forklift")
    register_asset("CV-07", "Conveyor")
    register_asset("", "Pallet Jack")
    register_asset("FL-01", "Crane")
    update_service_date("FL-01", "2025-01-15")
    update_service_date("XX-99", "2025-02-01")
    change_interval(-30)
    d = input("Last service date for CV-07 (YYYY-MM-DD, Enter to skip): ")
    if d:
        update_service_date("CV-07", d)
    assert len(assets) > 0, "no assets"
    printAlerts()
    export_service_report()
    write_scratch_copy()

main()
