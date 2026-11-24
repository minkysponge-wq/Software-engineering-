import datetime
import math

ZONE_RATES = {
    "BEG": 35.0,
    "INT": 60.0,
    "ADV": 85.0,
    "ALL": 110.0,
}


def parse_season_pass_validity(date_str):
    """Parse 'YYYY/MM/DD' and report whether the pass is valid (year >= 2026).

    Returns an error message string instead of raising on bad input.
    """
    # Fix: None / non-string input used to raise AttributeError on .split()
    if not isinstance(date_str, str):
        return "Invalid input: pass expiry must be a string in YYYY/MM/DD format"

    parts = date_str.strip().split('/')
    # Fix: missing/extra parts used to raise IndexError
    if len(parts) != 3:
        return "Invalid format: expected YYYY/MM/DD"

    # Fix: empty or non-numeric parts used to raise ValueError in int()
    try:
        year, month, day = (int(p.strip()) for p in parts)
    except ValueError:
        return "Invalid format: year, month and day must be whole numbers"

    # Fix: impossible dates (month 13, day 0, Feb 30, year 0/-5, ...) used to be
    # formatted as if they were real; validate against the real calendar.
    try:
        datetime.date(year, month, day)
    except (ValueError, OverflowError):
        return "Invalid date: no such calendar date"

    valid = year >= 2026
    return f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} ({'VALID' if valid else 'EXPIRED'})"


def compute_trail_gradient(elevation_str):
    """Return the gradient % for 'drop:distance', or None if the input is invalid."""
    # Fix: None / non-string input used to raise AttributeError
    if not isinstance(elevation_str, str):
        return None

    parts = elevation_str.split(':')
    # Fix: no ':' or several ':' used to raise ValueError on unpacking
    if len(parts) != 2:
        return None

    # Fix: empty / non-numeric values used to raise ValueError in float()
    try:
        drop = float(parts[0])
        distance = float(parts[1])
    except ValueError:
        return None

    # Fix: 'nan' / 'inf' were accepted and produced nan/inf results
    if not (math.isfinite(drop) and math.isfinite(distance)):
        return None
    # Fix: distance 0 used to raise ZeroDivisionError; negative distance is meaningless
    if distance <= 0:
        return None

    gradient_pct = (drop / distance) * 100.0
    # Fix: huge drop / tiny distance overflowed to inf
    if not math.isfinite(gradient_pct):
        return None
    return round(gradient_pct, 2)


def calculate_lift_access_tier(zone_code):
    """Return the lift pass price for a zone code, or None if the code is unknown."""
    # Fix: None / non-string input used to raise AttributeError on .strip()
    if not isinstance(zone_code, str):
        return None
    prefix = zone_code.strip().upper()[:3]
    # Fix: unknown/empty codes used to raise KeyError
    return ZONE_RATES.get(prefix)


def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    gradient = compute_trail_gradient(e_input)
    if gradient is None:
        print("Invalid input: expected two numbers 'drop:distance' with distance > 0")
    else:
        print("Gradient %:", gradient)

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    price = calculate_lift_access_tier(z_input)
    if price is None:
        print("Invalid zone code: use one of " + ", ".join(ZONE_RATES))
    else:
        print("Lift Pass Price: $", price)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nInput cancelled.")
