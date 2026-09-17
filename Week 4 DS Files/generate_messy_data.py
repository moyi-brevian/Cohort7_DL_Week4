"""
generate_messy_data.py
----------------------
TUTOR-ONLY SCRIPT. Do not show in class unless a student asks "where did
the data come from?" It reproducibly (fixed random seed) creates all
three files used this week:

    insurance_claims_messy.csv   -- main dataset: hand-logged claims,
                                     deliberately messy (missing values,
                                     outliers, inconsistent categories,
                                     mixed date formats, duplicates)
    policyholders.json           -- "system-exported" master data,
                                     cleaner than the claims log but
                                     still has a few realistic gaps
    exchange_rates_cache.json    -- a small cached fallback used by
                                     05_apis_and_files.py in case the
                                     classroom has no internet access
                                     when you fetch live USD/KES rates

Domain: Amani Insurance (fictional), a Kenyan motor/health/property
insurer with claims logged by assessors across six regional offices.

Run this file directly to (re)generate all three files:

    python generate_messy_data.py
"""

import csv
import json
import random
from datetime import date, timedelta

random.seed(7)  # reproducible "messiness" every time this is run

REGIONS = ["Nairobi", "Mombasa", "Kisumu", "Eldoret", "Nakuru", "Nyeri"]
# NOTE: only case/whitespace messiness here (no abbreviations like "Nrb").
# This week's scripts fix categories with a light .str.strip().str.title()
# pass rather than an explicit lookup table (that lookup-table pattern was
# Week 2's focus) -- so the messiness we inject needs to be the kind that
# a title-case pass can actually resolve.
REGION_VARIANTS = {
    "Nairobi": ["Nairobi", "NAIROBI", "nairobi", " Nairobi ", "NaIrObI"],
    "Mombasa": ["Mombasa", "MOMBASA", "mombasa ", "Mombasa ", "MOMBASA "],
    "Kisumu": ["Kisumu", "KISUMU", " kisumu", "Kisumu ", "KISUMU"],
    "Eldoret": ["Eldoret", "eldoret", "ELDORET ", "Eldoret ", "eldoret "],
    "Nakuru": ["Nakuru", "NAKURU", "nakuru ", " Nakuru", "NAKURU "],
    "Nyeri": ["Nyeri", "NYERI", "nyeri ", " Nyeri", "NYERI "],
}

CLAIM_TYPES = [
    "Motor-Accident", "Motor-Theft", "Health-Inpatient",
    "Health-Outpatient", "Property-Fire", "Property-Burglary",
]
CLAIM_TYPE_VARIANTS = {
    "Motor-Accident": ["Motor-Accident", "motor accident", "MOTOR-ACCIDENT", "Motor Accident "],
    "Motor-Theft": ["Motor-Theft", "motor theft", "MOTOR-THEFT ", "Motor Theft"],
    "Health-Inpatient": ["Health-Inpatient", "health inpatient", "HEALTH-INPATIENT", "Health Inpatient "],
    "Health-Outpatient": ["Health-Outpatient", "health outpatient", "HEALTH-OUTPATIENT ", "Health Outpatient"],
    "Property-Fire": ["Property-Fire", "property fire", "PROPERTY-FIRE", "Property Fire "],
    "Property-Burglary": ["Property-Burglary", "property burglary", "PROPERTY-BURGLARY ", "Property Burglary"],
}

# Roughly realistic KES claim-size ranges per claim type (mean, std)
CLAIM_TYPE_TYPICAL_AMOUNT = {
    "Motor-Accident": (180_000, 90_000),
    "Motor-Theft": (650_000, 200_000),
    "Health-Inpatient": (95_000, 60_000),
    "Health-Outpatient": (8_000, 4_000),
    "Property-Fire": (900_000, 400_000),
    "Property-Burglary": (250_000, 150_000),
}

STATUS_OPTIONS = ["Approved", "Rejected", "Pending", "Under Review"]
STATUS_VARIANTS = {
    "Approved": ["Approved", "approved", "APPROVED", "Approved "],
    "Rejected": ["Rejected", "rejected", "REJECTED ", "Rejected"],
    "Pending": ["Pending", "pending", "PENDING", " Pending"],
    "Under Review": ["Under Review", "under review", "UNDER REVIEW ", "under-review"],
}

ASSESSORS = ["J. Mwangi", "A. Otieno", "F. Wanjiru", "S. Kimani",
             "P. Achieng", "D. Cheruiyot", "L. Njeri", "M. Hassan"]

FIRST_NAMES = ["Brian", "Faith", "Kevin", "Grace", "Dennis", "Mercy",
               "Peter", "Ann", "James", "Lucy", "Samuel", "Diana",
               "Joseph", "Esther", "Collins", "Winnie"]
LAST_NAMES = ["Kariuki", "Odhiambo", "Mutiso", "Wafula", "Cherono",
              "Njoroge", "Onyango", "Kamau", "Barasa", "Wekesa"]

COVER_TYPES = ["Motor Comprehensive", "Motor Third-Party", "Health Cover",
               "Property Cover"]


def messy_amount(mean, std):
    """Return a claim amount as a string, with realistic dirtiness:
    occasional missing value, occasional thousands-comma formatting,
    a rare negative (data-entry sign error), and a rare wild outlier
    (an extra zero typed in by mistake)."""
    roll = random.random()
    if roll < 0.05:
        return ""  # missing amount
    value = max(500, round(random.gauss(mean, std), -2))
    if roll > 0.985:
        value *= 10  # fat-fingered outlier, e.g. 250,000 -> 2,500,000
    elif roll > 0.975:
        value = -value  # sign-entry error
    s = f"{value:,.0f}" if random.random() < 0.5 else f"{value:.0f}"
    return s


def messy_date(d):
    fmt = random.choice([
        "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%B %d, %Y", "%d.%m.%Y",
    ])
    return d.strftime(fmt)


def build_claims_rows(n_claims=500):
    header = ["claim_id", "policy_number", "claim_type", "claim_amount_kes",
              "claim_date", "region", "status", "assessor", "notes"]
    rows = []
    start = date(2024, 1, 1)

    policy_numbers = [f"AMI-{n:05d}" for n in range(1, 221)]  # 220 policyholders

    for i in range(1, n_claims + 1):
        claim_id = f"CLM-{i:05d}"
        policy_number = random.choice(policy_numbers)
        claim_type = random.choice(CLAIM_TYPES)
        mean, std = CLAIM_TYPE_TYPICAL_AMOUNT[claim_type]
        amount = messy_amount(mean, std)
        claim_date = start + timedelta(days=random.randint(0, 269))
        region = random.choice(REGIONS)
        status = random.choice(STATUS_OPTIONS)
        assessor = random.choice(ASSESSORS)
        notes = random.choice([
            "", "", "", "documents pending", "site visit done",
            "customer unreachable", "police abstract attached",
            "second opinion requested",
        ])

        rows.append([
            claim_id,
            policy_number,
            random.choice(CLAIM_TYPE_VARIANTS[claim_type]),
            amount,
            messy_date(claim_date),
            random.choice(REGION_VARIANTS[region]),
            random.choice(STATUS_VARIANTS[status]),
            assessor,
            notes,
        ])

    # a handful of exact duplicate rows (assessor double-submitted a form)
    for _ in range(9):
        rows.append(random.choice(rows).copy())

    random.shuffle(rows)
    return header, rows


def build_policyholders(n=220):
    """System-exported master data -- cleaner than the claims log, but
    still has a few realistic gaps (missing age/gender on older records)."""
    records = []
    start = date(2019, 1, 1)
    for i in range(1, n + 1):
        policy_number = f"AMI-{i:05d}"
        record = {
            "policy_number": policy_number,
            "full_name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
            "age": random.randint(19, 72) if random.random() > 0.04 else None,
            "gender": random.choice(["F", "M"]) if random.random() > 0.03 else None,
            "cover_type": random.choice(COVER_TYPES),
            "sum_insured_kes": random.choice([500_000, 800_000, 1_200_000,
                                               2_000_000, 3_500_000, 5_000_000]),
            "region": random.choice(REGIONS),
            "join_date": (start + timedelta(days=random.randint(0, 2000))).isoformat(),
        }
        records.append(record)
    return records


def build_exchange_rate_cache():
    """A small cached lookup of USD/KES rates for a handful of dates in
    the claims window, used as an offline fallback by
    05_apis_and_files.py if the live API call fails in class."""
    base = 129.5
    cache = {}
    d = date(2024, 1, 1)
    for _ in range(10):
        rate = round(base + random.uniform(-1.5, 1.5), 2)
        cache[d.isoformat()] = rate
        d += timedelta(days=27)
    return {"base": "USD", "target": "KES", "note": "offline fallback cache -- not live rates",
            "rates_by_date": cache}


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows to {path}")


def write_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Wrote {path}")


if __name__ == "__main__":
    claims_header, claims_rows = build_claims_rows()
    write_csv("insurance_claims_messy.csv", claims_header, claims_rows)

    write_json("policyholders.json", build_policyholders())
    write_json("exchange_rates_cache.json", build_exchange_rate_cache())
