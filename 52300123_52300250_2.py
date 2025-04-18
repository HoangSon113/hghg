import csv
import random
import pandas as pd
from datetime import datetime, timedelta

# PHẦN 1: TẠO TẬP DỮ LIỆU
def create_student_data():
    # Hàm tạo ngày sinh ngẫu nhiên
    def random_dob():
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2005, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_days = random.randrange(days_between_dates)
        return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

    # Danh sách tên người Việt
    first_names = ["Anh", "Bình", "Cường", "Dũng", "Hà", "Hải", "Hằng", "Hòa", "Hương", "Khánh", "Lan", "Linh", "Mai", "Minh", "Nam", "Ngọc", "Phúc", "Quân", "Tâm", "Thảo", "Sơn", "Kiệt"]
    last_names = ["Nguyễn Anh","Nguyễn Hoàng", "Lê Anh", "Bùi Thị Bích", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Vũ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Trương", "Đinh", "Phan", "Võ", "Tô", "Cao"]

    # Tạo tập dữ liệu
    data = []
    for i in range(20):
        x = random.randint(0, 4)
        yyy = random.randint(0, 500)
        student_id = f"52{x}00{yyy:03d}"
        student_name = f"{random.choice(last_names)} {random.choice(first_names)}"
        dob = random_dob()

        # Tạo điểm số (0-10)
        math_score = round(random.uniform(0.0, 10.0), 1)
        cs_score = round(random.uniform(0.0, 10.0), 1)
        eng_score = round(random.uniform(0.0, 10.0), 1)

        data.append([student_id, student_name, dob, math_score, cs_score, eng_score])

    # Ghi vào CSV
    with open('52300123_52300250_2.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['StudentID', 'StudentName', 'DayOfBirth', 'Math', 'CS', 'Eng'])
        writer.writerows(data)
    
    print("Đã tạo tập dữ liệu và lưu vào '52300123_52300250_2.csv'")
    return data

# PHẦN 2: ĐỊNH NGHĨA CÁC VỊ TỪ VÀ HÀM LƯỢNG TỬ
# Tải dữ liệu học sinh từ CSV
def load_student_data(filename='52300123_52300250_2.csv'):
    return pd.read_csv(filename, encoding='utf-8')

# Định nghĩa các vị từ
def is_passing(student):
    """Tất cả điểm số đều lớn hơn hoặc bằng 5."""
    return student['Math'] >= 5 and student['CS'] >= 5 and student['Eng'] >= 5

def is_high_math(student):
    """Điểm toán lớn hơn hoặc bằng 9."""
    return student['Math'] >= 9

def is_struggling(student):
    """Điểm toán và điểm tin học đều dưới 6."""
    return student['Math'] < 6 and student['CS'] < 6

def improved_in_cs(student):
    """Điểm tin học cao hơn điểm toán."""
    return student['CS'] > student['Math']

# Hàm lượng tử phổ dụng
def all_students_passed(df):
    """∀x is_passing(x): Tất cả học sinh đều đạt tất cả các môn."""
    return all(is_passing(student) for _, student in df.iterrows())

def all_students_math_above_3(df):
    """∀x (Math(x) > 3): Tất cả học sinh đều có điểm toán cao hơn 3."""
    return all(student['Math'] > 3 for _, student in df.iterrows())

# Hàm lượng tử tồn tại
def exists_high_math_student(df):
    """∃x is_high_math(x): Tồn tại một học sinh có điểm toán trên 9."""
    return any(is_high_math(student) for _, student in df.iterrows())

def exists_improved_cs_student(df):
    """∃x improved_in_cs(x): Tồn tại một học sinh có điểm tin học cao hơn điểm toán."""
    return any(improved_in_cs(student) for _, student in df.iterrows())

# Câu lệnh kết hợp/lồng nhau
def for_all_students_exists_subject_above_6(df):
    """∀x ∃s (Score(x,s) > 6): Đối với mỗi học sinh, tồn tại một môn học mà họ đạt điểm trên 6."""
    for _, student in df.iterrows():
        if not (student['Math'] > 6 or student['CS'] > 6 or student['Eng'] > 6):
            return False
    return True

def for_all_low_math_exists_subject_above_6(df):
    """∀x (Math(x) < 6 → ∃s (Score(x,s) > 6)): Đối với mỗi học sinh có điểm toán dưới 6, 
    tồn tại một môn học mà họ đạt điểm trên 6."""
    for _, student in df.iterrows():
        if student['Math'] < 6:
            if not (student['CS'] > 6 or student['Eng'] > 6):
                return False
    return True

# Hàm phủ định
def not_all_students_passed(df):
    """¬(∀x is_passing(x)): Không phải tất cả học sinh đều đạt tất cả các môn."""
    return not all_students_passed(df)

def not_all_students_math_above_3(df):
    """¬(∀x (Math(x) > 3)): Không phải tất cả học sinh đều có điểm toán cao hơn 3."""
    return not all_students_math_above_3(df)

def not_exists_high_math_student(df):
    """¬(∃x is_high_math(x)): Không tồn tại học sinh nào có điểm toán trên 9."""
    return not exists_high_math_student(df)

def not_exists_improved_cs_student(df):
    """¬(∃x improved_in_cs(x)): Không tồn tại học sinh nào có điểm tin học cao hơn điểm toán."""
    return not exists_improved_cs_student(df)

def not_for_all_students_exists_subject_above_6(df):
    """¬(∀x ∃s (Score(x,s) > 6)): Không phải với mọi học sinh, đều tồn tại một môn học mà họ đạt điểm trên 6."""
    return not for_all_students_exists_subject_above_6(df)

def not_for_all_low_math_exists_subject_above_6(df):
    """¬(∀x (Math(x) < 6 → ∃s (Score(x,s) > 6))): Không phải với mọi học sinh có điểm toán dưới 6,
    đều tồn tại một môn học mà họ đạt điểm trên 6."""
    return not for_all_low_math_exists_subject_above_6(df)

# PHẦN 3: CHƯƠNG TRÌNH CHÍNH
def main():
    # Tạo dữ liệu mới
    create_student_data()
    
    # Tải dữ liệu
    df = load_student_data()
    
    # Hiển thị dữ liệu
    print("\nTập dữ liệu Học sinh:")
    print(df)
    print("\n" + "="*80 + "\n")
    
    # Kiểm tra vị từ cho mỗi học sinh
    print("Vị từ cho mỗi học sinh:")
    for _, student in df.iterrows():
        print(f"Học sinh: {student['StudentName']} (ID: {student['StudentID']})")
        print(f"  Đạt tất cả môn: {is_passing(student)}")
        print(f"  Có điểm toán cao: {is_high_math(student)}")
        print(f"  Đang gặp khó khăn: {is_struggling(student)}")
        print(f"  Cải thiện về Tin học: {improved_in_cs(student)}")
        print("")
    print("="*80 + "\n")
    
    # Kiểm tra lượng tử phổ dụng
    print("Lượng tử Phổ dụng:")
    print(f"1. Tất cả học sinh đều đạt tất cả các môn: {all_students_passed(df)}")
    print(f"   Phủ định: Không phải tất cả học sinh đều đạt tất cả các môn: {not_all_students_passed(df)}")
    print(f"2. Tất cả học sinh đều có điểm toán cao hơn 3: {all_students_math_above_3(df)}")
    print(f"   Phủ định: Không phải tất cả học sinh đều có điểm toán cao hơn 3: {not_all_students_math_above_3(df)}")
    print("\n" + "="*80 + "\n")
    
    # Kiểm tra lượng tử tồn tại
    print("Lượng tử Tồn tại:")
    print(f"1. Tồn tại một học sinh đạt điểm toán trên 9: {exists_high_math_student(df)}")
    print(f"   Phủ định: Không có học sinh nào đạt điểm toán trên 9: {not_exists_high_math_student(df)}")
    print(f"2. Tồn tại một học sinh có điểm tin học cao hơn điểm toán: {exists_improved_cs_student(df)}")
    print(f"   Phủ định: Không có học sinh nào có điểm tin học cao hơn điểm toán: {not_exists_improved_cs_student(df)}")
    print("\n" + "="*80 + "\n")
    
    # Kiểm tra câu lệnh kết hợp/lồng nhau
    print("Câu lệnh Kết hợp/Lồng nhau:")
    print(f"1. Đối với mỗi học sinh, tồn tại một môn học mà họ đạt điểm trên 6: "
          f"{for_all_students_exists_subject_above_6(df)}")
    print(f"   Phủ định: Tồn tại một học sinh có điểm 6 hoặc thấp hơn ở tất cả các môn: "
          f"{not_for_all_students_exists_subject_above_6(df)}")
    print(f"2. Đối với mỗi học sinh có điểm toán dưới 6, tồn tại một môn học mà họ đạt điểm trên 6: "
          f"{for_all_low_math_exists_subject_above_6(df)}")
    print(f"   Phủ định: Tồn tại một học sinh có điểm toán dưới 6 và có điểm 6 hoặc thấp hơn ở tất cả các môn: "
          f"{not_for_all_low_math_exists_subject_above_6(df)}")
    
    # Giải thích về ý nghĩa của các phủ định bằng tiếng Anh đơn giản
    print("\n" + "="*80)
    print("GIẢI THÍCH Ý NGHĨA CÁC PHỦ ĐỊNH BẰNG TIẾNG ANH:")
    print("="*80)
    
    print("\n1. Negation of 'All students passed all subjects':")
    print("   - Original: All students passed all subjects.")
    print("   - Negation: Some students did not pass at least one subject.")
    
    print("\n2. Negation of 'All students have a math score higher than 3':")
    print("   - Original: All students have a math score higher than 3.")
    print("   - Negation: At least one student has a math score of 3 or lower.")
    
    print("\n3. Negation of 'There exists a student who scored above 9 in math':")
    print("   - Original: There is a student who scored above 9 in math.")
    print("   - Negation: No student scored above 9 in math.")
    
    print("\n4. Negation of 'There exists a student who improved in CS over Math':")
    print("   - Original: There is a student whose CS score is higher than their math score.")
    print("   - Negation: No student has a CS score higher than their math score.")
    
    print("\n5. Negation of 'For every student, there exists a subject in which they scored above 6':")
    print("   - Original: Every student has at least one subject with a score above 6.")
    print("   - Negation: At least one student has scores of 6 or lower in all subjects.")
    
    print("\n6. Negation of 'For every student scoring below 6 in Math, there exists a subject where they scored above 6':")
    print("   - Original: Every student with a math score below 6 has at least one subject with a score above 6.")
    print("   - Negation: At least one student with a math score below 6 has scores of 6 or lower in all subjects.")

if __name__ == "__main__":
    main()