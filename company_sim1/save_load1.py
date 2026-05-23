import json
from company1 import Company
from competitor1 import Competitor

def save_game(company, competitors):
    data = {
        "company": company.to_dict(),
        "competitors": [c.to_dict() for c in competitors]
    }
    with open("savefile.json", "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_game():
    with open("savefile.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    company = Company.from_dict(data["company"])
    competitors = [Competitor.from_dict(c) for c in data["competitors"]]

    return company, competitors