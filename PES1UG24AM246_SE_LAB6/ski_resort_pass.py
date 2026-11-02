def process_resort_bookings(groups, facility_fee):
    if not isinstance(groups, list) or facility_fee < 0:
        raise ValueError("Invalid groups list or facility fee")

    total_revenue = 0.0
    rejected_passes = 0

    for group in groups:
        if not group.get("is_active", False):
            continue

        pass_duration = group.get("duration", "full_day")
        skiers = group.get("skiers", [])

        if pass_duration == "season":
            base_rate = 300.0
        elif pass_duration == "full_day":
            base_rate = 80.0
        elif pass_duration == "half_day":
            base_rate = 50.0
        else:
            rejected_passes += 1
            continue

        group_total = 0.0

        for skier in skiers:
            age = skier.get("age", 0)
            gear_rental = skier.get("gear_rental", False)
            blackout_override = skier.get("blackout_override", False)

            if age <= 0:
                rejected_passes += 1
                continue

            if blackout_override:
                rejected_passes += 1
                if pass_duration == "half_day":
                    group_total = 0.0
                    break
                group_total += base_rate * 0.50
            elif age < 12:
                group_total += base_rate * 0.60
            elif age >= 65:
                group_total += base_rate * 0.70
            else:
                group_total += base_rate

            if gear_rental:
                group_total += 35.0

        if group.get("includes_lodge_locker", False):
            group_total += facility_fee

        total_revenue += group_total

    if rejected_passes > 4:
        return {"total_revenue": round(total_revenue, 2), "status": "AUDIT_REVIEW"}
    if total_revenue == 0.0:
        return {"total_revenue": 0.0, "status": "ZERO_SALES"}
    return {"total_revenue": round(total_revenue, 2), "status": "COMPLETED"}


def check_chairlift_anemometer(wind_streams):
    if not wind_streams:
        return "NO_DATA"

    for lift_readings in wind_streams:
        wind_gust_streak = 0
        for speed_mph in lift_readings:
            if speed_mph > 45:
                wind_gust_streak += 1
                if wind_gust_streak >= 2:
                    return "SUSPEND_LIFT"
            else:
                wind_gust_streak = 0
    return "SAFE_OPERATION"