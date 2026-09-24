"""Medicare Advantage benefits, Stars and county enrollment, joined, for Los Angeles County.

Reproduces the four-plan table from vladahealth.com/data/medicare-advantage/ca-los-angeles
through the REST API. Needs VLADA_API_KEY in the environment (free account with $5 of queries
at https://www.vladahealth.com/data-access).

Three clocks: enrollment is a report month, benefits are a plan year, Stars are a rating year.
Two keys: benefits and enrollment join on contract + plan id; Stars exist only for the contract.
"""
import json
import os
import urllib.request

API = "https://api.vladahealth.com/v1/tools"
KEY = os.environ["VLADA_API_KEY"]

PLANS = [  # contract, plan, name, April 2026 county enrollment (CMS CPSC)
    ("H0524", "003", "Kaiser Permanente Senior Advantage LA, Orange Co.", 178640),
    ("H5425", "006", "SCAN Classic", 82978),
    ("H0543", "168", "AARP Medicare Advantage from UHC CA-004P", 40647),
    ("H5619", "021", "Humana Gold Plus", 28111),
]


def call(tool: str, body: dict) -> dict:
    req = urllib.request.Request(
        f"{API}/{tool}", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def otc_line(resp: dict) -> str:
    """The filed OTC allowance, keeping 'offered with no amount filed' distinct from a number."""
    rows = [r for r in resp["value"]["rows"] if r.get("otc_sub_benefit") == "otc_items_allowance"]
    if not rows:
        return "no OTC allowance row"
    r = rows[0]
    if r["numeric_amount_observability"] == "all_offered_numeric":
        return (f"${r['benefit_amount']:g} {r['benefit_amount_period_label'].lower()}"
                f" (${r['benefit_amount_annualized']:g} a year; carries forward: {r['otc_cap_carry_forward_label']})")
    return f"{r['offered_status']}, no maximum amount filed ({r['null_amount_reason']})"


if __name__ == "__main__":
    for contract, plan, name, enrolled in PLANS:
        otc = call("get_pbp_benefit", {"contract_id": contract, "plan_id": plan,
                                       "payment_year": 2026, "category": "otc"})
        print(f"{name} ({contract}-{plan}) · {enrolled:,} members · OTC 2026: {otc_line(otc)}"
              f" · hash {otc['response_hash'][:8]}")
    # Stars are contract-level and are served on the MCP as get_stars(contract_id, year).
    # Ask your agent: "What is H0524's 2026 Star rating?" and it will call it.
