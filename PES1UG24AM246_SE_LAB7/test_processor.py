from hypothesis import given, settings, strategies as st
from processor import parse_season_pass_validity, compute_trail_gradient, calculate_lift_access_tier

# Inputs that look "almost right" so the fuzzer reaches deeper code paths
# (split/int/float/division/dict lookup), mixed with fully random text and None.
date_like = st.builds(
    lambda a, b, c: f"{a}/{b}/{c}",
    st.integers(-99999, 99999), st.integers(-50, 50), st.integers(-50, 50),
)
gradient_like = st.builds(
    lambda a, b: f"{a}:{b}",
    st.one_of(st.integers(-10000, 10000), st.floats(allow_nan=True, allow_infinity=True), st.text(max_size=5)),
    st.one_of(st.integers(-10000, 10000), st.floats(allow_nan=True, allow_infinity=True), st.text(max_size=5)),
)
zone_like = st.one_of(
    st.sampled_from(["BEG", "INT", "ADV", "ALL", "beg", "  int ", "advanced", "ALLZONES"]),
    st.text(max_size=6),
)


@settings(max_examples=300)
@given(st.text() | st.none() | date_like)
def test_parse_season_pass_validity_no_crash(s):
    try:
        result = parse_season_pass_validity(s)
        assert isinstance(result, str)
    except Exception as e:
        assert False, f"parse_season_pass_validity crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=300)
@given(st.text() | st.none() | gradient_like)
def test_compute_trail_gradient_safe(s):
    try:
        result = compute_trail_gradient(s)
        # Must return either a finite number or None for invalid input
        assert result is None or (isinstance(result, float) and result == result
                                  and result not in (float("inf"), float("-inf"))), \
            f"compute_trail_gradient returned invalid value {result!r} for {s!r}"
    except Exception as e:
        assert False, f"compute_trail_gradient crashed on {s!r} with: {type(e).__name__}: {e}"


@settings(max_examples=300)
@given(st.text() | st.none() | zone_like)
def test_calculate_lift_access_tier_safe(s):
    try:
        result = calculate_lift_access_tier(s)
        assert result is None or result in (35.0, 60.0, 85.0, 110.0), \
            f"calculate_lift_access_tier returned unexpected value {result!r} for {s!r}"
    except Exception as e:
        assert False, f"calculate_lift_access_tier crashed on {s!r} with: {type(e).__name__}: {e}"


# Sanity checks: valid inputs must still give the right answers after hardening.
def test_valid_inputs_still_work():
    assert parse_season_pass_validity("2027/03/15") == "Pass Expiry: 2027-03-15 (VALID)"
    assert parse_season_pass_validity("2025/03/15") == "Pass Expiry: 2025-03-15 (EXPIRED)"
    assert compute_trail_gradient("250:1000") == 25.0
    assert calculate_lift_access_tier("beg") == 35.0
    assert calculate_lift_access_tier("  ALL ") == 110.0
