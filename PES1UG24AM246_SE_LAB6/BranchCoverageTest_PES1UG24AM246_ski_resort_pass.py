"""Branch coverage tests for ski_resort_pass.py.

Goal: every decision (if / elif / loop) evaluates both True and False.
Includes all line-coverage scenarios plus targeted tests for each branch
outcome and the boundary values of every comparison.
"""

import pytest
from ski_resort_pass import process_resort_bookings, check_chairlift_anemometer


def booking(duration="full_day", skiers=None, locker=False, active=True):
    """Build a single-group booking list."""
    return [{"is_active": active, "duration": duration,
             "includes_lodge_locker": locker,
             "skiers": skiers if skiers is not None else []}]


# ---------- input validation: line 2 ----------

def test_invalid_groups_type_raises():
    with pytest.raises(ValueError):
        process_resort_bookings("not a list", 10.0)


def test_negative_facility_fee_raises():
    with pytest.raises(ValueError):
        process_resort_bookings([], -1.0)


def test_zero_facility_fee_is_valid():
    # boundary: fee == 0 must not raise
    result = process_resort_bookings(booking(skiers=[{"age": 30}]), 0.0)
    assert result == {"total_revenue": 80.0, "status": "COMPLETED"}


# ---------- outer loop: line 8 ----------

def test_empty_groups_list_gives_zero_sales():
    # loop body never runs
    assert process_resort_bookings([], 15.0) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- is_active: line 9 ----------

def test_inactive_group_skipped():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30}], active=False), 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_missing_is_active_defaults_to_inactive():
    groups = [{"duration": "full_day", "skiers": [{"age": 30}]}]
    assert process_resort_bookings(groups, 15.0)["status"] == "ZERO_SALES"


# ---------- duration: lines 15-23 ----------

@pytest.mark.parametrize("duration, expected", [
    ("season", 300.0),
    ("full_day", 80.0),
    ("half_day", 50.0),
])
def test_each_valid_duration_base_rate(duration, expected):
    result = process_resort_bookings(
        booking(duration, [{"age": 30}]), 15.0)
    assert result == {"total_revenue": expected, "status": "COMPLETED"}


def test_missing_duration_defaults_to_full_day():
    groups = [{"is_active": True, "skiers": [{"age": 30}]}]
    assert process_resort_bookings(groups, 15.0)["total_revenue"] == 80.0


def test_unknown_duration_rejected():
    result = process_resort_bookings(booking("weekly", [{"age": 30}]), 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


# ---------- skier loop: line 27 ----------

def test_group_with_no_skiers_only_pays_locker():
    # skier loop never runs; locker still charged
    result = process_resort_bookings(booking(skiers=[], locker=True), 15.0)
    assert result == {"total_revenue": 15.0, "status": "COMPLETED"}


def test_missing_skiers_key_defaults_to_empty():
    groups = [{"is_active": True, "duration": "full_day"}]
    assert process_resort_bookings(groups, 15.0)["status"] == "ZERO_SALES"


# ---------- age validation: line 32 ----------

@pytest.mark.parametrize("age", [0, -5])
def test_non_positive_age_rejected(age):
    result = process_resort_bookings(booking(skiers=[{"age": age}]), 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_missing_age_defaults_to_zero_and_rejected():
    result = process_resort_bookings(booking(skiers=[{}]), 15.0)
    assert result["status"] == "ZERO_SALES"


# ---------- blackout override: lines 36-41 ----------

def test_blackout_full_day_half_price():
    result = process_resort_bookings(
        booking("full_day", [{"age": 30, "blackout_override": True}]), 15.0)
    assert result == {"total_revenue": 40.0, "status": "COMPLETED"}


def test_blackout_season_half_price():
    result = process_resort_bookings(
        booking("season", [{"age": 30, "blackout_override": True}]), 15.0)
    assert result["total_revenue"] == 150.0


def test_blackout_half_day_resets_group_and_breaks():
    # earlier skier's 50 is wiped out; later skier is never priced
    skiers = [{"age": 30},
              {"age": 30, "blackout_override": True},
              {"age": 30}]
    result = process_resort_bookings(booking("half_day", skiers), 15.0)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_blackout_half_day_still_charges_locker_after_break():
    result = process_resort_bookings(
        booking("half_day", [{"age": 30, "blackout_override": True}],
                locker=True), 15.0)
    assert result == {"total_revenue": 15.0, "status": "COMPLETED"}


# ---------- age categories: lines 42-47 (with boundaries) ----------

@pytest.mark.parametrize("age, expected", [
    (1, 48.0),    # child, lowest valid age
    (11, 48.0),   # child, just below 12
    (12, 80.0),   # adult, boundary
    (64, 80.0),   # adult, just below 65
    (65, 56.0),   # senior, boundary
    (90, 56.0),   # senior
])
def test_age_category_pricing(age, expected):
    result = process_resort_bookings(booking(skiers=[{"age": age}]), 15.0)
    assert result["total_revenue"] == expected


# ---------- gear rental: line 49 ----------

def test_gear_rental_adds_fee():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30, "gear_rental": True}]), 15.0)
    assert result["total_revenue"] == 115.0


def test_no_gear_rental_no_fee():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30, "gear_rental": False}]), 15.0)
    assert result["total_revenue"] == 80.0


def test_blackout_with_gear_still_charges_gear():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30, "gear_rental": True,
                         "blackout_override": True}]), 15.0)
    assert result["total_revenue"] == 75.0


# ---------- lodge locker: line 52 ----------

def test_locker_adds_facility_fee():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30}], locker=True), 15.0)
    assert result["total_revenue"] == 95.0


def test_no_locker_no_facility_fee():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30}], locker=False), 15.0)
    assert result["total_revenue"] == 80.0


# ---------- final status: lines 57-61 ----------

def test_exactly_four_rejections_not_audited():
    result = process_resort_bookings(
        booking(skiers=[{"age": 0}] * 4 + [{"age": 30}]), 15.0)
    assert result == {"total_revenue": 80.0, "status": "COMPLETED"}


def test_five_rejections_triggers_audit():
    result = process_resort_bookings(
        booking(skiers=[{"age": 0}] * 5 + [{"age": 30}]), 15.0)
    assert result == {"total_revenue": 80.0, "status": "AUDIT_REVIEW"}


def test_rejections_counted_across_groups():
    groups = (booking("weekly", [{"age": 30}]) * 3
              + booking(skiers=[{"age": 0}, {"age": 0}]))
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 0.0, "status": "AUDIT_REVIEW"}


def test_revenue_rounded_to_two_decimals():
    result = process_resort_bookings(
        booking(skiers=[{"age": 30}], locker=True), 10.555)
    assert result["total_revenue"] == 90.56


def test_mixed_booking_all_groups():
    groups = [
        {"is_active": False, "duration": "season", "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "season",
         "includes_lodge_locker": True,
         "skiers": [
             {"age": 8, "gear_rental": True},
             {"age": 70, "gear_rental": True},
             {"age": 30, "gear_rental": True},
             {"age": 0, "gear_rental": True},
             {"age": 40, "gear_rental": True, "blackout_override": True},
         ]},
        {"is_active": True, "duration": "half_day",
         "includes_lodge_locker": True,
         "skiers": [{"age": 25, "blackout_override": True}]},
        {"is_active": True, "duration": "weekly", "skiers": [{"age": 30}]},
        {"is_active": True, "duration": "full_day",
         "includes_lodge_locker": True,
         "skiers": [{"age": 30, "gear_rental": True}]},
    ]
    result = process_resort_bookings(groups, 15.0)
    assert result == {"total_revenue": 1140.0, "status": "COMPLETED"}


# ---------- check_chairlift_anemometer ----------

@pytest.mark.parametrize("streams", [[], None])
def test_anemometer_no_data(streams):
    assert check_chairlift_anemometer(streams) == "NO_DATA"


def test_anemometer_two_consecutive_gusts_suspend():
    assert check_chairlift_anemometer([[46, 46]]) == "SUSPEND_LIFT"


def test_anemometer_single_gust_is_safe():
    assert check_chairlift_anemometer([[50]]) == "SAFE_OPERATION"


def test_anemometer_exactly_45_is_not_a_gust():
    assert check_chairlift_anemometer([[45, 45, 45]]) == "SAFE_OPERATION"


def test_anemometer_gust_streak_resets():
    assert check_chairlift_anemometer([[50, 30, 50]]) == "SAFE_OPERATION"


def test_anemometer_streak_resets_then_suspends():
    assert check_chairlift_anemometer([[50, 30, 50, 50]]) == "SUSPEND_LIFT"


def test_anemometer_streak_does_not_carry_across_lifts():
    # gust at end of lift 1 + gust at start of lift 2 is not a streak
    assert check_chairlift_anemometer([[10, 50], [50, 10]]) == "SAFE_OPERATION"


def test_anemometer_second_lift_suspends():
    assert check_chairlift_anemometer([[10, 20], [47, 48]]) == "SUSPEND_LIFT"


def test_anemometer_empty_lift_readings_safe():
    assert check_chairlift_anemometer([[], []]) == "SAFE_OPERATION"
