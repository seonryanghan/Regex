
import re

with open("07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt",
          "r", encoding="utf-8") as file:
    text = file.read()

email_pattern = r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?![A-Za-z0-9.-])"
emails = re.findall(email_pattern, text)

phone_pattern = r"(?<!\d)010(?:[-. ]\d{4}){2}(?!\d)"
phones = re.findall(phone_pattern, text)

student_pattern = r"\[(202\d{6})\s*/\s*([^\]\r\n]+)\]"
students = re.findall(student_pattern, text)

github_pattern = r"https?://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+(?:\.git)?/?"
github_urls = re.findall(github_pattern, text)

coupon_pattern = r"\bFEST-2026-[A-Z0-9]{4}\b"
coupons = re.findall(coupon_pattern, text)

sales_pattern = r"매출:\s*([\d,]+)\s*원"
sales = re.findall(sales_pattern, text)

sales = [int(amount.replace(",", "")) for amount in sales]

total_sales = sum(sales)

print("1. 이메일")
print(emails)

print("\n2. 휴대폰 번호")
print(phones)

print("\n3. 학번 및 학과")
print(students)

print("\n4. GitHub 저장소")
print(github_urls)

print("\n5. 유효 쿠폰")
print(coupons)

print("\n6. 부스별 매출")
for amount in sales:
    print(f"{amount:,}원")

print(f"\n전체 매출 합계: {total_sales:,}원")
