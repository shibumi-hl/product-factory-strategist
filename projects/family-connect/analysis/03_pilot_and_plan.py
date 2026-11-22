"""Option C: pilot sample size, recruitment time, acquisition funnel, payback limit, year-3 landmark.
Inputs: brief (F) and model assumptions (H, E-073/E-074). Run: py -3 analysis/03_pilot_and_plan.py
"""
from math import ceil, log

Z_A, Z_B = 1.96, 0.84          # alpha 0.05 two-sided, power 0.80 (convention)
CON_START = 6500               # E-005 connected groups at start of planned year
HH_ACCESS = 100_000            # E-002

def n_per_arm(p1, p2):
    return ceil((Z_A + Z_B) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2)

print("== 1. Pilot sample (unit = family group, primary metric = restriction within 7 days) ==")
for label, p1, p2 in [("base: 12 % -> 9 % (E-013)", .12, .09), ("smaller: 12 % -> 10 %", .12, .10),
                      ("unfavourable: 12 % -> 10.5 %", .12, .105)]:
    n = n_per_arm(p1, p2)
    print(f"{label}: {n} groups per arm, {2*n} total")

print("\n== 2. Recruitment: first-time eligible groups ==")
for sc, elig, members, p_low in [("base", .70, 2.0, .25), ("unfavourable", .55, 1.5, .15)]:
    pool = CON_START * elig
    p_group_month = 1 - (1 - p_low) ** members        # >=1 member with low balance in a month
    weekly = 1 - (1 - p_group_month) ** (12 / 52)
    print(f"{sc}: eligible pool {pool:.0f} groups; P(group has first event in a month) {p_group_month:.0%}")
    for need in (n_per_arm(.12, .09) * 2, n_per_arm(.12, .10) * 2):
        if need >= pool:
            print(f"  need {need}: exceeds pool {pool:.0f} -> not reachable in pilot without new groups")
            continue
        weeks = log(1 - need / pool) / log(1 - weekly)
        print(f"  need {need}: {weeks:.1f} weeks of recruitment + 1 week observation")
    for w in (6, 10):
        got = pool * (1 - (1 - weekly) ** w)
        print(f"  after {w} weeks: {got:.0f} first-time eligible groups")

print("\n== 3. Acquisition funnel (base / unfavourable), from month 8 ==")
for sc, app, conv, acc, sup in [("base", .60, .05, .65, 400), ("unfavourable", .45, .025, .50, 150)]:
    reach = (HH_ACCESS - CON_START) * app
    created = reach * conv
    accepted = created * acc
    print(f"{sc}: households not yet connected {HH_ACCESS-CON_START}; see offer {reach:.0f}; create group {created:.0f}; "
          f"invite accepted {accepted:.0f}; + support {sup} = {accepted+sup:.0f} new connected groups")

print("\n== 4. Payback limit per person-month ==")
team_pm = {"developers (Q2 3 + Q3 1)": 4, "designer 0.5 x 9 months": 4.5, "analyst 0.5 x 12 months": 6, "QA": 1}
total = sum(team_pm.values())
for sc, limit in [("base", 3.38), ("unfavourable", 0.37)]:   # E-081
    print(f"{sc}: recoverable by end of year 2 {limit} mln RUB / {total} person-months = "
          f"{limit*1e6/total:,.0f} RUB per person-month max fully loaded cost")
print("team:", team_pm)

print("\n== 5. Year-3 landmark ==")
for share in (0.15, 0.20):
    print(f"connected families {share:.0%} of 100 000 accessible households = {share*HH_ACCESS:.0f} groups "
          f"(planned-year base forecast 10 373 = {10373/HH_ACCESS:.1%})")
