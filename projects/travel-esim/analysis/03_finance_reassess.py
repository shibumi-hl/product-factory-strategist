"""Reassess option C with the finance note (travel-esim).

Inputs copied from sources/finance-note-2026-11.md (PM's own material, marked test data):
  item 1  wholesale 48 RUB/GB + 3% payment processing (Turkey, UAE, Egypt)   -> E-031
  item 2  roaming data revenue per trip that buys a package, 2025: 1,250 RUB -> E-032
  item 3  share of subscriber trips abroad with a roaming package, 2025: 22% -> E-033
  item 4  share of base with eSIM-capable phone, Oct 2026: 41%               -> E-034
Public inputs: E-001 tourist trips 13.4 mln; E-021 independent range 52-82 RUB/GB.
Hypotheses (H): our subscriber share of trips 20/25/30 %; 41% of the base used as the
eSIM-capable share of travellers; 20% holdout; 3% take-rate; 10 GB pack.
"""
WHOLESALE, FEE, ROAM_REV, ROAM_SHARE, ESIM = 48, 0.03, 1250, 0.22, 0.41
GB, TRIPS, TARGET = 10, 13.4e6, 300_000

print("1. Margin and break-even cannibalisation k_max = margin / 1,250 RUB, 10 GB pack")
print("price_RUB_per_GB  pack_price  margin_RUB  k_max")
for ppgb in (52, 60, 70, 79, 82):
    p = ppgb * GB
    m = p - WHOLESALE * GB - FEE * p
    print(f"{ppgb:16d}  {p:10d}  {m:10.0f}  {m/ROAM_REV:5.1%}")
p = 790
m = p - WHOLESALE * GB - FEE * p
print(f"Planned price 790: margin {m:.0f} RUB, k_max {m/ROAM_REV:.1%}; "
      f"package-buying share of trips today {ROAM_SHARE:.0%}")
print(f"Net gain per buyer if buyers mirror all trips (k = {ROAM_SHARE:.0%}): {m - ROAM_SHARE*ROAM_REV:.0f} RUB")
for k in (0.10, 0.30, 0.50):
    print(f"Net gain per buyer if k = {k:.0%}: {m - k*ROAM_REV:.0f} RUB")

print("\n2. Pilot volume and 300k take-rate with eSIM-capable share 41% (was 30-70% scenarios)")
for s in (0.20, 0.25, 0.30):
    elig = TRIPS * s * ESIM
    exp = elig * 0.8
    print(f"sub share {s:.0%}: eligible {elig/1e6:.2f} mln, exposed {exp/1e6:.2f} mln, "
          f"3% take = {exp*0.03/1e3:.0f}k, 300k needs {TARGET/elig:.1%} of eligible trips")

print("\n3. Sensitivity to negotiated wholesale cost at the planned 790 RUB pack")
for w in (36, 40, 44, 48):
    m = 790 - w * GB - FEE * 790
    print(f"wholesale {w} RUB/GB: margin {m:.0f} RUB, k_max {m/ROAM_REV:.1%}")
