"""Sizing and price-per-GB checks for travel-esim.

Inputs are copied from ledger rows (no files in sources/; public data only):
  E-001 tourist trips 2025 = 13.4 mln; all-purpose trips = 31.5 mln
  E-006 independent travel eSIM, Turkey: 10 GB for 520-820 RUB
  E-014 MTS 'Bit za granitsu' Turkey: 1290 RUB / 10 GB / 14 days
  E-015 Beeline 'Mir' 1590 RUB / 10 GB / 14 days; MegaFon 'Zabugorye' 1590 RUB / 10 GB / 14 days
Scenario parameters (our subscriber share of trips, eSIM-capable share) are hypotheses (H).
"""
TARGET = 300_000
TRIPS = {"tourist trips 2025 [E-001]": 13.4e6, "all-purpose trips 2025 [E-001]": 31.5e6}
SUB_SHARE = [0.20, 0.25, 0.30]      # (H) our share of travellers
ESIM_CAPABLE = [0.30, 0.50, 0.70]   # (H) share of those travellers with eSIM-capable phone

print("Required take-rate (paid activations / eligible trips) to hit 300k in 12 months")
for name, trips in TRIPS.items():
    print(f"\n{name}: {trips/1e6:.1f} mln trips; target = {TARGET/trips:.2%} of ALL trips")
    print("sub_share  esim_cap  eligible_trips_mln  required_take_rate")
    for s in SUB_SHARE:
        for c in ESIM_CAPABLE:
            elig = trips * s * c
            print(f"{s:>9.0%}  {c:>8.0%}  {elig/1e6:>18.2f}  {TARGET/elig:>18.1%}")

print("\nPrice per GB, Turkey, 10 GB packs (RUB/GB)")
prices = {"independent eSIM low [E-006]": 520, "independent eSIM high [E-006]": 820,
          "MTS Bit za granitsu [E-014]": 1290, "Beeline Mir [E-015]": 1590,
          "MegaFon Zabugorye [E-015]": 1590}
for k, v in prices.items():
    print(f"{k:32s} {v/10:7.0f}")
lo, hi = 520 / 10, 820 / 10
print(f"Operator packages cost {1290/820:.1f}x-{1590/520:.1f}x the independent eSIM price per GB")
