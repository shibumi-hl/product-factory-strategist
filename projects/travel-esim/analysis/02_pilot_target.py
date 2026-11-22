"""Pilot target and break-even cannibalisation for option C (travel-esim).

Inputs copied from ledger rows (public data only; no files in sources/):
  E-001 tourist trips 2025 = 13.4 mln
  E-006 / E-021 independent eSIM, Turkey 10 GB = 520-820 RUB (52-82 RUB/GB)
  E-014 MTS 'Bit za granitsu' Turkey 1290 RUB / 10 GB / 14 d
  E-015 Beeline / MegaFon Turkey packages 1590 RUB / 10 GB / 14 d
Scenario parameters are hypotheses (H), chosen by us, not sourced:
  subscriber share 20/25/30 %, eSIM-capable 30/50/70 % (as in 01_sizing.py),
  holdout 20 % of eligible subscribers (to measure cannibalisation),
  pilot take-rate 1.5 / 3 / 5 % of exposed eligible trips,
  wholesale cost 20 / 35 / 50 RUB per GB (finance has no figure; P4 open).
"""
TOURIST_TRIPS = 13.4e6
SCEN = {"low": (0.20, 0.30), "mid": (0.25, 0.50), "high": (0.30, 0.70)}
HOLDOUT = 0.20
TAKE = [0.015, 0.03, 0.05]

print("1. Paid activations in 12 months = tourist trips x sub share x eSIM-capable x (1-holdout) x take-rate")
print("scenario  eligible_mln  exposed_mln  " + "  ".join(f"take {t:.1%}" for t in TAKE))
for name, (s, c) in SCEN.items():
    elig = TOURIST_TRIPS * s * c
    exp = elig * (1 - HOLDOUT)
    print(f"{name:8s}  {elig/1e6:12.2f}  {exp/1e6:11.2f}  " + "  ".join(f"{exp*t/1e3:8.0f}k" for t in TAKE))

mid_exp = TOURIST_TRIPS * 0.25 * 0.50 * (1 - HOLDOUT)
print(f"\nProposed target: 3% of mid-scenario exposed trips = {mid_exp*0.03/1e3:.0f}k activations")
print(f"Share of 300k brief target: {mid_exp*0.03/300_000:.0%}; "
      f"remainder for E = {(300_000-mid_exp*0.03)/1e3:.0f}k = {(300_000-mid_exp*0.03)/TOURIST_TRIPS:.2%} of tourist trips")
holdout_mid = TOURIST_TRIPS * 0.25 * 0.50 * HOLDOUT
print(f"Holdout size, mid scenario: {holdout_mid/1e3:.0f}k eligible trips")

print("\n2. Break-even cannibalisation k_max = eSIM margin / roaming package revenue replaced")
print("   (10 GB Turkey pack priced at 790 RUB, i.e. 79 RUB/GB, inside the independent range 52-82)")
PRICE, GB = 790, 10
print("cost_RUB_per_GB  margin_RUB  k_max_vs_1290  k_max_vs_1590")
for cost in (20, 35, 50):
    m = PRICE - cost * GB
    print(f"{cost:15d}  {m:10d}  {m/1290:13.0%}  {m/1590:13.0%}")
