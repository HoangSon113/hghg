import csv
import pandas as pd

# Đọc file CSV
try:
    df = pd.read_csv("52300123_52300250_2.csv")
except FileNotFoundError:
    print("Lỗi: Không tìm thấy file .csv")
    exit()

# Định nghĩa vị từ
predicates = {
    'Qua tất cả môn': lambda s: s[['Math', 'CS', 'Eng']].ge(5).all(),
    'Toán cao': lambda s: s['Math'] >= 9,
    'Khó khăn': lambda s: (s['Math'] < 6) & (s['CS'] < 6),
    'Cải thiện CS': lambda s: s['CS'] > s['Math']
}

# Hàm định lượng
quantifiers = [
    ('tat_ca_qua_mon', 'Tất cả học sinh qua tất cả môn', predicates['Qua tất cả môn'], 'all'),
    ('tat_ca_toan_tren_3', 'Tất cả học sinh có Math > 3', lambda s: s['Math'] > 3, 'all'),
    ('ton_tai_toan_cao', 'Tồn tại học sinh có Math ≥ 9', predicates['Toán cao'], 'exists'),
    ('ton_tai_cai_thien_cs', 'Tồn tại học sinh cải thiện CS', predicates['Cải thiện CS'], 'exists'),
    ('moi_nguoi_co_mon_cao', 'Mọi học sinh có môn > 6', 
     lambda df: all(s[['Math', 'CS', 'Eng']].gt(6).any() for _, s in df.iterrows()), 'custom'),
    ('toan_thap_co_mon_cao', 'Học sinh Math < 6 có môn > 6', 
     lambda df: all(s[['CS', 'Eng']].gt(6).any() if s['Math'] < 6 else True for _, s in df.iterrows()), 'custom')
]

# Giải thích phủ định bằng tiếng Anh
negation_explanations = {
    'tat_ca_qua_mon': ("All students passed all subjects.", "Some students failed at least one subject."),
    'tat_ca_toan_tren_3': ("All students have Math score > 3.", "At least one student has Math score ≤ 3."),
    'ton_tai_toan_cao': ("There exists a student with Math ≥ 9.", "No student has Math ≥ 9."),
    'ton_tai_cai_thien_cs': ("There exists a student with CS > Math.", "No student has CS > Math."),
    'moi_nguoi_co_mon_cao': ("Every student has at least one subject > 6.", "Some student has all subjects ≤ 6."),
    'toan_thap_co_mon_cao': (
        "Every student with Math < 6 has another subject > 6.",
        "Some student with Math < 6 has all other subjects ≤ 6."
    )
}

def evaluate_quantifier(key, pred, quant, df):
    """Đánh giá phát biểu định lượng"""
    if quant == 'all':
        return all(pred(row) for _, row in df.iterrows())
    elif quant == 'exists':
        return any(pred(row) for _, row in df.iterrows())
    else:  # custom
        return pred(df)

def evaluate_negation(key, pred, quant, df):
    """Đánh giá phủ định của phát biểu định lượng"""
    return not evaluate_quantifier(key, pred, quant, df)

def main():
    print("\nKết quả các phát biểu định lượng:")
    results = {}
    for key, desc, pred, quant in quantifiers:
        result = evaluate_quantifier(key, pred, quant, df)
        results[key] = result
        print(f"{desc}: {result}")

    print("\nKết quả các phát biểu phủ định:")
    for key, desc, pred, quant in quantifiers:
        neg_result = evaluate_negation(key, pred, quant, df)
        print(f"Phủ định: Không {desc.lower()}: {neg_result}")

    print("\nGiải thích phủ định (tiếng Anh):")
    for key, (orig, neg) in negation_explanations.items():
        print(f"\n{key.replace('_', ' ').title()}:")
        print(f"  Original: {orig}")
        print(f"  Negation: {neg}")

if __name__ == "__main__":
    main()