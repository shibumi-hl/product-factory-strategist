"""Planned-year model for the strategic options (base and unfavourable scenarios).
Brief figures are F (E-IDs in comments). Every other parameter is an assumption (H)
with a range; public anchors are cited. Run: py -3 analysis/02_options_model.py
Calendar: month 1 = January of the planned year. Pilot runs Q2 (months 4-6) on half of
eligible units (randomised); scale-up from month 8 after the end-of-Q2 decision.
"""

RUB_PER_MONTH = 500          # E-008
GP_NC, GP_TGT = 279.0, 285.0 # E-003, mln RUB
CON_START, CON_NC, CON_TGT = 6500, 8000, 12000  # E-005
ACT_NC, ACT_TGT = 5000, 8000 # E-004
OWN_START, OWN_NC, OWN_TGT = 800, 1000, 2000    # E-006
HH_ACCESS, OWN_ACCESS = 100_000, 40_000         # E-002

# share of a month during which the service is live for treated units
def treated_months():
    # pilot: months 4-6 at 50 % of eligible; months 8-12 at 100 %; month 7 = decision/rollout at 50 %
    return [0, 0, 0, .5, .5, .5, .5, 1, 1, 1, 1, 1]

def in_year_months_from(month):
    """Average paid months remaining in the year for a unit added in `month` (1..12)."""
    return 12 - month + 0.5

SCEN = {
 "base": dict(
    # --- family signal option (C) ---
    eligible_tariff=0.70,      # H: share of connected groups on tariffs allowing the transfer
    members=2.0,               # H: participants per group besides organizer (brief: up to 5 at real operator E-025)
    p_low=0.25,                # H: share of member-months with a low-balance event
    restr_base=0.12,           # H: restriction within 7 days of first low-balance case (brief example E-013)
    restr_cut=0.03,            # H: −3 pp (to 9 %), brief example threshold E-013
    lapse_months=0.5,          # H: extra paid months per prevented restriction (10 % lapse × ~5 months)
    app_share=0.60,            # H: households reachable in app at the right moment (push opt-in ~50 % E-058)
    offer_conv=0.05,           # H: offer → group created (push CTR 2-4 % E-054/E-055; contextual in-app higher E-061)
    accept=0.65,               # H: invitation accepted within 14 days (brief example 60 % is illustrative)
    support_groups=400,        # H: groups created from support offers during 'relative ran out' contacts
    exits_cut=150,             # H: group exits avoided because members stay connected
    new_number_share=0.20,     # H: share of new member numbers that are new to the operator
    active_share=0.70,         # H: active share of connected groups with signal (no change 62.5 % E-070)
    act14=0.55,                # H: 14-day activation with signal + clearer invite (no change 45 % E-007)
    # --- owners payment reminder option (D) ---
    p_susp=0.06,               # H: monthly share of owners' second (router) numbers suspended for non-payment
    susp_cut=0.30,             # H: relative cut by reminder 3 days before billing date (E-042 qualitative)
    owner_lapse=0.6,           # H: extra paid months per prevented suspension
    owner_link=1000,           # H: extra owners linking 2+ numbers via reminder prompt
    # --- auto-share tariff rule option (F) ---
    auto_cut=0.06,             # H: restriction 12 % → 6 % when pool has free volume
    pool_free=0.6,             # H: share of low events when the pool has enough free volume
    cannibal=0.15,             # H: lost add-on package months per prevented restriction (sold before)
    auto_active=0.66,          # H: active share; automatic allocations may count as activity
 ),
 "unfavourable": dict(
    eligible_tariff=0.55, members=1.5, p_low=0.15, restr_base=0.12, restr_cut=0.015,
    lapse_months=0.2, app_share=0.45, offer_conv=0.025, accept=0.50, support_groups=150,
    exits_cut=50, new_number_share=0.10, active_share=0.65, act14=0.48,
    p_susp=0.03, susp_cut=0.15, owner_lapse=0.3, owner_link=400,
    auto_cut=0.04, pool_free=0.4, cannibal=0.30, auto_active=0.63,
 ),
}

def option_C(s):
    tm = treated_months()
    avg_groups = (CON_START + CON_NC) / 2
    members_elig = avg_groups * s["eligible_tariff"] * s["members"]
    prevented = sum(members_elig * s["p_low"] * s["restr_cut"] * t for t in tm)
    m_restr = prevented * s["lapse_months"]
    # acquisition: in-app offer from month 8, spread evenly over months 8-12
    reach = (HH_ACCESS - CON_START) * s["app_share"]
    created_app = reach * s["offer_conv"]
    new_groups = created_app * s["accept"] + s["support_groups"]
    m_new = 0
    for mth in range(8, 13):
        g = new_groups / 5
        m_new += g * s["members"] * s["new_number_share"] * in_year_months_from(mth)
    connected = CON_NC + new_groups + s["exits_cut"]
    active = connected * s["active_share"]
    months = m_restr + m_new
    return dict(connected=connected, active=active, act14=s["act14"], owners=OWN_NC,
                prevented=prevented, months=months, m_restr=m_restr, m_new=m_new,
                gp=GP_NC + months * RUB_PER_MONTH / 1e6)

def option_D(s):
    tm = treated_months()
    prevented = sum(OWN_ACCESS * s["p_susp"] * s["susp_cut"] * t for t in tm)
    months = prevented * s["owner_lapse"]
    return dict(connected=CON_NC, active=ACT_NC, act14=0.45, owners=OWN_NC + s["owner_link"],
                prevented=prevented, months=months, m_restr=months, m_new=0,
                gp=GP_NC + months * RUB_PER_MONTH / 1e6)

def option_F(s):
    tm = treated_months()
    avg_groups = (CON_START + CON_NC) / 2
    members_elig = avg_groups * s["eligible_tariff"] * s["members"]
    prevented = sum(members_elig * s["p_low"] * s["pool_free"] * s["auto_cut"] * t for t in tm)
    months = prevented * (s["lapse_months"] - s["cannibal"])
    connected = CON_NC + s["exits_cut"] * 1.5
    return dict(connected=connected, active=connected * s["auto_active"], act14=0.47, owners=OWN_NC,
                prevented=prevented, months=months, m_restr=months, m_new=0,
                gp=GP_NC + months * RUB_PER_MONTH / 1e6)

def show(name, r):
    print(f"{name}: connected {r['connected']:.0f} | active {r['active']:.0f} ({r['active']/r['connected']:.1%}) | "
          f"act14 {r['act14']:.0%} | owners {r['owners']:.0f} | prevented events {r['prevented']:.0f} | "
          f"extra paid months {r['months']:.0f} (restr {r['m_restr']:.0f}, new numbers {r['m_new']:.0f}) | "
          f"GP {r['gp']:.2f} mln (gap to 285: {GP_TGT-r['gp']:.2f})")

print("A STATUS-QUO: connected 8000 | active 5000 (62.5%) | act14 45% | owners 1000 | GP 279.00 (gap 6.00)  [E-003..E-007]")
for sc, s in SCEN.items():
    print(f"\n=== scenario: {sc} ===")
    rc, rd, rf = option_C(s), option_D(s), option_F(s)
    show("C family signal + one-tap transfer", rc)
    show("D owners payment-day reminder   ", rd)
    show("F auto-share tariff rule        ", rf)
    show("C+D-lite (D at SMS only, no cabinet)", dict(rc, owners=rd["owners"], months=rc["months"] + rd["months"],
         m_restr=rc["m_restr"] + rd["m_restr"], gp=GP_NC + (rc["months"] + rd["months"]) * RUB_PER_MONTH / 1e6))

print("\n=== break-even: what C would need to close the 6 mln gap alone ===")
s = SCEN["base"]
need = 12000  # E-072
rc = option_C(s)
print(f"base C gives {rc['months']:.0f} months; missing {need-rc['months']:.0f}")
print(f"  e.g. new groups needed if each brings {s['members']*s['new_number_share']:.2f} new numbers × ~3 months: "
      f"{(need-rc['m_restr'])/(s['members']*s['new_number_share']*3):.0f}")
print(f"  or lapse months per prevented restriction needed: {(need-rc['m_new'])/rc['prevented']:.1f} (base {s['lapse_months']})")

print("\n=== investment limit (development + launch), payback by end of year 2 ===")
for sc, s in SCEN.items():
    for nm, f in (("C", option_C), ("D", option_D)):
        r = f(s)
        y1 = r["months"] * RUB_PER_MONTH / 1e6
        # year 2: full-year run rate of the Dec monthly effect, no further growth (conservative)
        dec = r["months"] / sum(treated_months())
        y2 = dec * 12 * RUB_PER_MONTH / 1e6
        print(f"{sc:13s} {nm}: year-1 GP +{y1:.2f} mln; year-2 run-rate +{y2:.2f} mln; "
              f"max recoverable investment by end of year 2 ≈ {y1+y2:.2f} mln RUB")
