"""Corrected model after red-team review (2026-11-22). Supersedes 02 and parts of 03.
Changes: (1) acquisition campaign M is a separate lever available to any option;
(2) C pilot pool limited by member consent and free volume; realistic dates (build in Q2,
launch 1 June); (3) higher active share only for groups the signal can reach;
(4) D treated base = owners who actually have a device/router SIM; D-lite has fewer links;
(5) payback per option with its own team size. Run: py -3 analysis/04_corrected_model.py
"""
from math import ceil, log, sqrt

RUB = 500                                  # E-008
GP_NC = 279.0                              # E-003
CON_START, CON_NC = 6500, 8000             # E-005
ACT_NC = 5000                              # E-004
OWN_NC = 1000                              # E-006
HH_ACCESS, OWN_ACCESS = 100_000, 40_000    # E-002
Z = 1.96 + 0.84

S = {
 "base": dict(elig=.70, consent=.50, free=.70, members=2.0, p_low=.25, restr=.12, cut=.03, lapse=.5,
              act_uplift=.15, reach=.60, conv_signal=.05, conv_plain=.025, accept=.65, support=400,
              new_num=.20, router=.50, p_susp=.06, susp_cut=.30, owner_lapse=.6, link_full=1000, link_lite=300),
 "unfavourable": dict(elig=.55, consent=.30, free=.50, members=1.5, p_low=.15, restr=.12, cut=.015, lapse=.2,
              act_uplift=.05, reach=.45, conv_signal=.025, conv_plain=.0125, accept=.50, support=150,
              new_num=.10, router=.25, p_susp=.03, susp_cut=.15, owner_lapse=.3, link_full=400, link_lite=100),
}
# C: build Apr-May, launch 1 June to 50 % (pilot), read effect end of Sept, scale from October
TM_C = [0, 0, 0, 0, 0, .5, .5, .5, .5, 1, 1, 1]
# D: smaller build, launch 1 May to 50 %, scale from August
TM_D = [0, 0, 0, 0, .5, .5, .5, 1, 1, 1, 1, 1]
TEAM = {"C": 15.5, "D": 6.0, "C+D": 18.0}  # person-months incl. design, analytics, QA (H)

def campaign(s, conv):
    """Acquisition campaign from August (months 8-12), applicable to any option."""
    groups = (HH_ACCESS - CON_START) * s["reach"] * conv * s["accept"] + s["support"] * (conv / s["conv_signal"])
    months = sum(groups / 5 * s["members"] * s["new_num"] * (12 - m + .5) for m in range(8, 13))  # unit added in month m pays (12-m+0.5) months
    return groups, months

def signal(s):
    reach_share = s["elig"] * s["consent"] * s["free"]
    avg_groups = (CON_START + CON_NC) / 2
    members_reached = avg_groups * reach_share * s["members"]
    prevented = sum(members_reached * s["p_low"] * s["cut"] * t for t in TM_C)
    return reach_share, prevented, prevented * s["lapse"]

def owners(s, lite):
    base = OWN_ACCESS * s["router"]
    prevented = sum(base * s["p_susp"] * s["susp_cut"] * t for t in TM_D)
    return base, prevented, prevented * s["owner_lapse"], (s["link_lite"] if lite else s["link_full"])

def row(name, con, act, own, months):
    gp = GP_NC + months * RUB / 1e6
    print(f"{name:32s} connected {con:6.0f} | active {act:5.0f} | owners {own:5.0f} | +months {months:5.0f} | GP {gp:6.2f}")
    return gp

for sc, s in S.items():
    print(f"\n=== {sc} ===")
    rs, prev, m_sig = signal(s)
    g_plain, m_plain = campaign(s, s["conv_plain"])
    g_sig, m_sigcamp = campaign(s, s["conv_signal"])
    obase, oprev, m_own, _ = owners(s, False)
    print(f"C reach: {rs:.0%} of connected groups get signals; prevented restrictions {prev:.0f} -> {m_sig:.0f} months")
    print(f"campaign: without signal argument {g_plain:.0f} groups/{m_plain:.0f} months; with signal argument {g_sig:.0f}/{m_sigcamp:.0f}")
    print(f"D base {obase:.0f} owner device numbers; prevented suspensions {oprev:.0f} -> {m_own:.0f} months")
    act_share = ACT_NC / CON_NC
    def active(con, signal_on):
        return con * act_share + (con * rs * s["act_uplift"] if signal_on else 0)
    row("A status quo", CON_NC, ACT_NC, OWN_NC, 0)
    row("M campaign only (any option)", CON_NC + g_plain, active(CON_NC + g_plain, False), OWN_NC, m_plain)
    row("C signal only", CON_NC, active(CON_NC, True), OWN_NC, m_sig)
    row("C signal + campaign", CON_NC + g_sig, active(CON_NC + g_sig, True), OWN_NC, m_sig + m_sigcamp)
    row("D owners reminder (full)", CON_NC, ACT_NC, OWN_NC + s["link_full"], m_own)
    row("D-lite (SMS) + campaign", CON_NC + g_plain, active(CON_NC + g_plain, False), OWN_NC + s["link_lite"], m_own + m_plain)
    row("C + campaign + D-lite", CON_NC + g_sig, active(CON_NC + g_sig, True), OWN_NC + s["link_lite"], m_sig + m_sigcamp + m_own)
    print("signal's own incremental contribution (C+campaign minus campaign only): "
          f"groups {g_sig-g_plain:.0f}, months {m_sig+m_sigcamp-m_plain:.0f}, "
          f"active {active(CON_NC+g_sig, True)-active(CON_NC+g_plain, False):.0f}")
    # pilot feasibility
    pool = CON_START * rs
    p_grp = 1 - (1 - s["p_low"]) ** s["members"]
    wk = 1 - (1 - p_grp) ** (12 / 52)
    for weeks in (8, 13):
        n = pool * (1 - (1 - wk) ** weeks)
        mde = Z * sqrt(2 * .12 * .88 / (n / 2))
        print(f"C pilot: pool {pool:.0f} groups; after {weeks} weeks {n:.0f} first-time eligible -> detectable effect ≈{mde*100:.1f} pp (from 12 %)")
    # payback by end of year 2 (year-2 = December monthly effect x 12, retention parts only; campaign months grow, use Dec run-rate)
    for nm, months, tm in (("C signal only", m_sig, TM_C), ("D full", m_own, TM_D)):
        dec = months / sum(tm)
        lim = (months + dec * 12) * RUB / 1e6
        team = TEAM["C" if nm.startswith("C") else "D"]
        print(f"payback limit {nm}: {lim:.2f} mln RUB by end of year 2 -> {lim*1e6/team:,.0f} RUB per person-month ({team} pm)")
