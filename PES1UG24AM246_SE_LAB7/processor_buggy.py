def parse_season_pass_validity(date_str):
    parts = date_str.split('/')
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2])
    valid = year >= 2026 and 1 <= month <= 12 and 1 <= day <= 31
    return f"Pass Expiry: {year:04d}-{month:02d}-{day:02d} ({'VALID' if valid else 'EXPIRED'})"

def compute_trail_gradient(elevation_str):
    drop_str, dist_str = elevation_str.split(':')
    drop = float(drop_str)
    distance = float(dist_str)
    gradient_pct = (drop / distance) * 100.0
    return round(gradient_pct, 2)

def calculate_lift_access_tier(zone_code):
    prefix = zone_code.strip().upper()[:3]
    zone_rates = {
        "BEG": 35.0,
        "INT": 60.0,
        "ADV": 85.0,
        "ALL": 110.0
    }
    return zone_rates[prefix]

def main():
    print("==== Running parse_season_pass_validity ====")
    d_input = input("Enter pass expiry (YYYY/MM/DD): ")
    print(parse_season_pass_validity(d_input))

    print("\n==== Running compute_trail_gradient ====")
    e_input = input("Enter drop:distance (e.g. 250:1000): ")
    print("Gradient %:", compute_trail_gradient(e_input))

    print("\n==== Running calculate_lift_access_tier ====")
    z_input = input("Enter zone code (e.g. BEG, INT, ALL): ")
    print("Lift Pass Price: $", calculate_lift_access_tier(z_input))

if __name__ == "__main__":
    main()