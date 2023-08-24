from datetime import datetime

# Recap's mocks________________________________________________
# 2023 Base, whithout alterd days
RECAP_BASE_YEAR = {
    "name": 2023,
    "number_of_days": 365,
    "mornings": 72,
    "evenings": 73,
    "nights": 75,
    "workings": 220,
    "frees": 145,
    "holidays": 15,
    "extra_holidays": 6,
    "holidays_not_worked": 9,
    "change_payables": 0,
    "keep_days": 0,
    "overtimes": 0,
    "laborals": 260,
    "days_weekend": 105,
}

# 2023 November Team C Base, whithout alterd days
RECAP_BASE_MONTH = {
    "name": "Noviembre",
    "number_of_days": 30,
    "mornings": 4,
    "evenings": 5,
    "nights": 7,
    "workings": 16,
    "frees": 14,
    "holidays": 1,
    "extra_holidays": 1,
    "holidays_not_worked": 0,
    "change_payables": 0,
    "keep_days": 0,
    "overtimes": 0,
    "laborals": 22,
    "days_weekend": 8,
}
# MOCKS to:  test_alter_day_recap
DATE_TEST = datetime.strptime("2023-11-08", "%Y-%m-%d")
