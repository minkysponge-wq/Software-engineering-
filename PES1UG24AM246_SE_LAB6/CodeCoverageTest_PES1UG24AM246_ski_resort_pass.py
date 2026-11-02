"""Code (line) coverage tests for ski_resort_pass.py.

Goal: execute every statement at least once. Scenarios are combined, so
some decision outcomes (e.g. no gear rental, no locker) are never taken;
those are covered in BranchCoverageTest_PES1UG24AM246_ski_resort_pass.py.
"""

import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


# ---------- process_resort_bookings ----------

def test_invalid_groups_type_raises():
    with pytest.raises(ValueError):
        process_resort_bookings("not a list", 10.0)


def test_negative_facility_fee_raises():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1.0)


def test_mixed_booking_executes_every_pricing_line():
    groups = [
        # inactive group -> skipped
        {"is_active": False, "duration": "season",
         "skiers": [{"age": 30}]},
        # season: child, senior, adult, invalid age, blackout; all with gear
        {"is_active": True, "duration": "season",
         "includes_lodge_locker": True,
         "skiers": [
             {"age": 8, "gear_rental": True},                 # 180 + 35
             {"age": 70, "gear_rental": True},                # 210 + 35
             {"age": 30, "gear_rental": True},                # 300 + 35
             {"age": 0, "gear_rental": True},                 # rejected
             {"age": 40, "gear_rental": True,
              "blackout_override": True},                     # 150 + 35, rejected
         ]},                                                  # + 15 locker
        # half day blackout -> group total reset to 0, loop breaks
        {"is_active": True, "duration": "half_day",
         "includes_lodge_locker": True,
         "skiers": [{"age": 25, "blackout_override": True}]},  # 0 + 15, rejected
        # unknown duration -> rejected
        {"is_active": True, "duration": "weekly",
         "skiers": [{"age": 30}]},
        # full day adult with gear and locker
        {"is_active": True, "duration": "full_day",
         "includes_lodge_locker": True,
         "skiers": [{"age": 30, "gear_rental": True}]},        # 80 + 35 + 15
    ]
    result = process_resort_bookings(groups, 15.0)
    # 995 (season) + 15 (half day) + 130 (full day); 4 rejections
    assert result == {"total_revenue": 1140.0, "status": "COMPLETED"}


def test_more_than_four_rejections_triggers_audit():
    groups = [{"is_active": True, "duration": "full_day",
               "skiers": [{"age": 0}] * 5}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_only_inactive_groups_gives_zero_sales():
    groups = [{"is_active": False, "duration": "full_day",
               "skiers": [{"age": 30}]}]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- check_chairlift_anemometer ----------

def test_anemometer_no_data():
    assert check_chairlift_anemometer([]) == "NO_DATA"


def test_anemometer_streak_resets_then_suspends():
    # 50 (streak 1) -> 30 (reset) -> 50, 50 (streak 2) -> suspend
    assert check_chairlift_anemometer([[50, 30, 50, 50]]) == "SUSPEND_LIFT"


def test_anemometer_calm_readings_safe():
    assert check_chairlift_anemometer([[10, 20, 30]]) == "SAFE_OPERATION"
