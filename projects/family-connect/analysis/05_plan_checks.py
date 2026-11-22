"""Chosen plan (C reframed + offer A/B + D-lite): test sizes and payback.
Inputs: E-088 (H) and outputs of 04_corrected_model.py (E-090..E-093). Run: py -3 analysis/05_plan_checks.py
"""
from math import ceil

Z = 1.96 + 0.84
RUB = 500                 # E-008

def n_arm(p1, p2):
    return ceil(Z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2)

print("== 1. Offer A/B: does the promise of alerts raise group creation? (unit = household shown the offer) ==")
for sc, plain, sig in [("base", .05 / 2, .05), ("unfavourable", .025 / 2, .025)]:
    n = n_arm(plain, sig)
    weekly = 93_500 * 0.60 / 13      # E-088: 60 % of unconnected households reachable; spread over a quarter
    print(f"{sc}: {plain:.2%} vs {sig:.2%} -> {n} households per arm, {2*n} total; "
          f"≈{2*n/weekly:.1f} weeks at ≈{weekly:.0f} reachable households per week")

print("\n== 2. D-lite pilot: suspension of owners' device numbers (unit = owner-month) ==")
for sc, p, cut, base in [("base", .06, .30, 20_000), ("unfavourable", .03, .15, 10_000)]:
    n = n_arm(p, p * (1 - cut))
    months = 2 * n / (base / 2)      # half of device numbers in pilot, one observation per month
    print(f"{sc}: {p:.1%} -> {p*(1-cut):.2%}: {n} owner-months per arm; ≈{months:.1f} billing months with {base//2} numbers in pilot")

print("\n== 3. Payback of the chosen plan by end of year 2 ==")
CHURN = 0.015            # H: monthly churn of an ordinary number (US postpaid ~0.9 % E-034; prepaid higher)
TEAM_PM = 15.5           # dev 4 (Q2 3 incl. C 2 + D-lite 1, Q3 1), design 4.5, analytics 6, QA 1
for sc, m_y1, groups, new_share, members, m_ret_dec in [
        ("base", 3694, 2223, .20, 2.0, (67 + 1404) / 8.5),      # E-093; retention months per treated month
        ("unfavourable", 343, 676, .10, 1.5, (2 + 88) / 8.5)]:
    new_numbers = groups * members * new_share
    y2_new = sum(new_numbers * (1 - CHURN) ** m for m in range(1, 13))
    y2_ret = m_ret_dec * 12
    total = (m_y1 + y2_new + y2_ret) * RUB / 1e6
    print(f"{sc}: year 1 +{m_y1} months ({m_y1*RUB/1e6:.2f} mln); year 2 new numbers {y2_new:.0f} + retention {y2_ret:.0f} months; "
          f"recoverable by end of year 2 ≈ {total:.2f} mln RUB -> ≤ {total*1e6/TEAM_PM:,.0f} RUB per person-month ({TEAM_PM} pm)")
