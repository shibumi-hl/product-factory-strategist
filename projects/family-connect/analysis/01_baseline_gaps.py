"""Baseline gap decomposition from the brief's figures only.
Inputs typed from the ledger; each with its E-ID. Run: py -3 analysis/01_baseline_gaps.py
"""

# E-004 active family groups (last month of year)
ACT_BASE_PLAN, ACT_BASE_EST, ACT_NC, ACT_TGT = 5000, 4000, 5000, 8000
# E-005 connected family groups at year end
CON_BASE_PLAN, CON_BASE_EST, CON_NC, CON_TGT = 7500, 6500, 8000, 12000
# E-006 connected multi-number owners
OWN_BASE_EST, OWN_NC, OWN_TGT = 800, 1000, 2000
# E-003 gross profit, mln RUB
GP_NC, GP_TGT = 279, 285
# E-008 RUB of gross profit per extra paid month per number
RUB_PER_MONTH = 500
# E-002 accessible base
HH_ACCESS, OWN_ACCESS = 100_000, 40_000

def pct(x):
    return f"{x*100:.1f} %"

print("== 1. Base year: why 4 000 active instead of 5 000 ==")
share_plan = ACT_BASE_PLAN / CON_BASE_PLAN
share_est = ACT_BASE_EST / CON_BASE_EST
vol = (CON_BASE_EST - CON_BASE_PLAN) * share_plan
rate = CON_BASE_EST * (share_est - share_plan)
print(f"active share: plan {pct(share_plan)}, estimate {pct(share_est)}")
print(f"gap {ACT_BASE_EST-ACT_BASE_PLAN}: volume effect {vol:.0f}, rate effect {rate:.0f} "
      f"(volume {vol/(vol+rate):.0%} / rate {rate/(vol+rate):.0%})")

print("\n== 2. Planned year: what the target requires ==")
print(f"no-change active share {pct(ACT_NC/CON_NC)}; target share {pct(ACT_TGT/CON_TGT)}")
print(f"connected: net growth to target {CON_TGT-CON_BASE_EST}; gap vs no-change {CON_TGT-CON_NC}")
print(f"active gap vs no-change {ACT_TGT-ACT_NC}: from volume at no-change share "
      f"{(CON_TGT-CON_NC)*ACT_NC/CON_NC:.0f}, from share uplift {CON_TGT*(ACT_TGT/CON_TGT-ACT_NC/CON_NC):.0f}")
for con in (8000, 10000, 12000):
    print(f"  if connected = {con}: active at 62.5 % = {con*0.625:.0f}; share needed for 8 000 = {pct(ACT_TGT/con)}")

print("\n== 3. Coverage of accessible base ==")
for name, n, base in [("families base-est", CON_BASE_EST, HH_ACCESS), ("families no-change", CON_NC, HH_ACCESS),
                      ("families target", CON_TGT, HH_ACCESS), ("owners base-est", OWN_BASE_EST, OWN_ACCESS),
                      ("owners no-change", OWN_NC, OWN_ACCESS), ("owners target", OWN_TGT, OWN_ACCESS)]:
    print(f"{name}: {n} / {base} = {pct(n/base)}")

print("\n== 4. Profit gap ==")
gap_rub = (GP_TGT - GP_NC) * 1e6
months = gap_rub / RUB_PER_MONTH
print(f"gap {GP_TGT-GP_NC} mln RUB = {months:.0f} extra paid number-months at {RUB_PER_MONTH} RUB")
for months_left in (12, 9, 6, 3):
    print(f"  if effect runs {months_left} months of the year: {months/months_left:.0f} numbers kept paying every month")
