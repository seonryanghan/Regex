
# 정규표현식 사용을 위한 내장 모듈 호출
import re

# 텍스트를 추출할 파일 불러오기
with open("07-02. 전주대 대동제 및 해커톤 통합운영 데이터 로그.txt",
          "r", encoding="utf-8") as file:
    text = file.read()
"r" 읽기 모드로 파일열기
encoding ="utf-8" 문자 깨짐 방지를 위한 문자 형식 지정\
text = file.read() 파일 전체를 읽어옴

1. 이메일 추출 코드
email_pattern = r"(?<![A-Za-z0-9._%+-])[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9])?@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z]{2,}(?![A-Za-z0-9.-])"
emails = re.findall(email_pattern, text)

이메일 아이디와 도메인 부분을 검사 
도메인 라벨은 영문 또는 숫자로
시작해야 하므로 `hyunwoo@.ac.kr`처럼 `@` 바로 뒤에 마침표가 오는 주소는 제외
-   `[A-Za-z0-9]`: 영문 대소문자 또는 숫자
-   `[A-Za-z0-9._%+-]`: 이메일 아이디에 사용할 수 있는 문자 집합
-   `@`: 아이디와 도메인의 구분 기호
-   `\.`: 실제 마침표
-   `[A-Za-z]{2,}`: 영문 2글자 이상의 최상위 도메인
-   `(?<!...)`: 앞쪽에 지정한 문자가 없는지 검사하는 부정형 후방 탐색
-   `(?!...)`: 뒤쪽에 지정한 문자가 없는지 검사하는 부정형 전방 탐색

2. 전화번호 추출 코드
phone_pattern = r"(?<!\d)010(?:[-. ]\d{4}){2}(?!\d)"
phones = re.findall(phone_pattern, text)

010으로 시작하고 중간 4자리, 끝 4자리인 번호를 추출 
숫자 묶음 사이에는 하이픈(`-`), 마침표(`.`), 공백을 허용함

-   `010`: 반드시 010으로 시작
-   `[-. ]`: 하이픈, 마침표 또는 공백 중 하나
-   `\d{4}`: 숫자 4자리
-   `(?:...)`: 추출 그룹으로 저장하지 않는 비캡처 그룹
-   `{2}`: 앞의 그룹을 두 번 반복
-   `(?<!\d)` / `(?!\d)`: 번호 앞뒤에 숫자가 붙지 않도록 검사

3. 학번 및 학과 추출 코드
student_pattern = r"\[(202\d{6})\s*/\s*([^\]\r\n]+)\]"
students = re.findall(student_pattern, text)

대괄호 안의 `[학번 / 학과]` 형식에서 202로 시작하는 9자리 학번과
학과명을 각각 추출

-   `\[` / `\]`: 실제 여는 대괄호와 닫는 대괄호
-   `(202\d{6})`: 202로 시작하는 9자리 학번을 첫 번째 그룹으로 추출
-   `\s*`: 공백이 0개 이상
-   `/`: 학번과 학과 사이의 슬래시
-   `([^\]\r\n]+)`: 닫는 대괄호나 줄바꿈이 아닌 문자를 학과명으로 추출

캡처 그룹이 두 개이므로 결과는 `(학번, 학과)` 튜플의 리스트가 결과로 나옴

4-1. github 저장소 url 추출 코드
github_pattern = r"https?://github\.com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+(?:\.git)?/?"
github_urls = re.findall(github_pattern, text)

`github.com` 도메인의 저장소 URL을 추출합니다. `gitlab.com`은 도메인이
일치하지 않아 제외됩니다.

-   `https?`: `http` 또는 `https`
-   `github\.com`: GitHub 도메인
-   `[A-Za-z0-9-]+`: 사용자 또는 조직 이름
-   `[A-Za-z0-9_.-]+`: 저장소 이름
-   `(?:\.git)?`: `.git` 확장자가 있을 수도 있음
-   `/?`: 마지막 슬래시가 있을 수도 있음

4-2. 2026년 유효 쿠폰코드 추출 코드
coupon_pattern = r"\bFEST-2026-[A-Z0-9]{4}\b"
coupons = re.findall(coupon_pattern, text)

`FEST-2026-`으로 시작하고 영문 대문자 또는 숫자 4자리가 이어지는 쿠폰
코드를 추출 따라서 2025년도 쿠폰은 제외됨

-   `\b`: 단어 경계
-   `[A-Z0-9]`: 영문 대문자 또는 숫자
-   `{4}`: 정확히 4자리 반복

5. 부스별 총 매출액 추출 및 합산 코드
sales_pattern = r"매출:\s*([\d,]+)\s*원"
sales = re.findall(sales_pattern, text)

sales = [int(amount.replace(",", "")) for amount in sales]

total_sales = sum(sales)
정산 내역에서 `매출:` 뒤에 표시된 금액만 추출
카드·현금 세부금액은 총매출에 포함되어 있으므로 별도로 더하지 않음

-   `매출:`: 매출이라는 고정 문자열
-   `\s*`: 공백이 0개 이상
-   `([\d,]+)`: 숫자와 쉼표로 구성된 금액을 추출 그룹으로 지정
-   `\s*원`: 선택적 공백 뒤에 `원`이 오는지 확인
-   `replace(",", "")`: 금액의 쉼표 제거
-   `int()`: 문자열을 정수로 변환
-   `sum()`: 모든 매출액 합산

# 추출한 이메일 출력
print("1. 이메일")
print(emails)

# 추출한 전화번호 출력
print("\n2. 휴대폰 번호")
print(phones)

# 추출한 학번 및 학과 출력
print("\n3. 학번 및 학과")
print(students)

# 추출한 github url 출력
print("\n4. GitHub 저장소")
print(github_urls)

# 추출한 유효 쿠폰 출력
print("\n5. 유효 쿠폰")
print(coupons)

# 부스별 매출 및 전채 매출 합계 출력
print("\n6. 부스별 매출")
for amount in sales:
    print(f"{amount:,}원")

print(f"\n전체 매출 합계: {total_sales:,}원")
