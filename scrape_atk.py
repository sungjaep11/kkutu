import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import time

initials = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

base_urls = [
    "https://kkukowiki.kr/w/공격단어/한국어/",
    "https://kkukowiki.kr/w/방어단어/한국어/"
]

headers = {"User-Agent": "Mozilla/5.0"}
all_words = []

for base_url in base_urls:
    for ch in initials:
        url = base_url + urllib.parse.quote(ch)
        print(f"📥 크롤링 중: {url}")
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ 실패: {url} - {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        for table in tables:
            headers_th = table.find_all("th")
            if not headers_th:
                continue

            header_texts = [th.get_text(strip=True) for th in headers_th]
            if "단어" not in header_texts:
                continue

            word_col_index = header_texts.index("단어")
            rows = table.find_all("tr")[1:]

            for row in rows:
                cols = row.find_all("td")
                if len(cols) > word_col_index:
                    word = cols[word_col_index].get_text(strip=True)
                    if word:
                        all_words.append(word)

        time.sleep(1)  # 서버에 부담을 줄이기 위한 대기

# ✅ 중복 제거 (등장 순서 유지)
unique_words = list(dict.fromkeys(all_words))

# 저장
with open("atk_words.json", "w", encoding="utf-8") as f:
    json.dump(unique_words, f, ensure_ascii=False, indent=2)

print(f"\n✅ 중복 제거 후 {len(unique_words)}개의 단어를 atk_words.json에 저장했습니다.")
