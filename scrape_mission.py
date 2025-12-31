import requests
from bs4 import BeautifulSoup
import json
import urllib.parse

# 초성 목록: ㄱ~ㅎ
initials = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

base_url = "https://kkukowiki.kr/w/미션_단어/한국어/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_words = []

for ch in initials:
    # URL 인코딩 필요
    url = base_url + urllib.parse.quote(ch)
    print(f"크롤링 중: {url}")
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"❌ 접근 실패: {url}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    for table in tables:
        headers_th = table.find_all("th")
        if not headers_th:
            continue

        # "단어" 열이 있는 테이블만 처리
        header_texts = [th.get_text(strip=True) for th in headers_th]
        if "단어" not in header_texts:
            continue

        word_col_index = header_texts.index("단어")

        # 각 행에서 "단어" 열 값 추출
        rows = table.find_all("tr")[1:]  # 헤더 제외
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > word_col_index:
                word = cols[word_col_index].get_text(strip=True)
                if word:
                    all_words.append(word)

# 결과 저장 (중복 제거 없이 순서 그대로)
with open("mission_words.json", "w", encoding="utf-8") as f:
    json.dump(all_words, f, ensure_ascii=False, indent=2)

print(f"\n✅ 총 {len(all_words)}개의 단어를 mission_words.json에 저장했습니다.")
