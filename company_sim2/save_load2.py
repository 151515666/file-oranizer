import json
import os

from company import Company
from employee import Employee
from product import Product
from competitor import Competitor

SAVE_FILE = "save_data.json"


def save_game(company, competitors, filepath=SAVE_FILE):
    """게임 상태를 JSON 파일로 저장"""
    data = {
        "company": company.to_dict(),
        "company_employees": [e.to_dict() for e in company.employees],
        "company_products": [p.to_dict() for p in company.products],
        "competitors": [c.to_dict() for c in competitors],
    }
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"저장 완료: {filepath}")


def load_game(filepath=SAVE_FILE):
    """JSON 파일에서 게임 상태를 복원"""
    if not os.path.exists(filepath):
        print("저장 파일이 없습니다.")
        return None, None

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # company 복원
    company = Company.from_dict(data["company"])
    company.employees = [Employee.from_dict(e) for e in data["company_employees"]]
    company.products = [Product.from_dict(p) for p in data["company_products"]]

    # competitors 복원
    competitors = [Competitor.from_dict(c) for c in data["competitors"]]

    print(f"불러오기 완료: {filepath}")
    return company, competitors


def delete_save(filepath=SAVE_FILE):
    """저장 파일 삭제"""
    if os.path.exists(filepath):
        os.remove(filepath)
        print("저장 파일을 삭제했습니다.")
    else:
        print("삭제할 저장 파일이 없습니다.")


def save_exists(filepath=SAVE_FILE):
    """저장 파일 존재 여부 확인"""
    return os.path.exists(filepath)
