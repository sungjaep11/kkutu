import requests
from bs4 import BeautifulSoup
import json
import urllib.parse
import os
import time

# 저장할 폴더 이름
save_dir = "long_words"

# 폴더가 없으면 생성
os.makedirs(save_dir, exist_ok=True)

initials = ['ㄱ','ㄴ','ㄷ','ㄹ','ㅁ','ㅂ','ㅅ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']
base_url = "https://kkukowiki.kr/w/긴_단어/한국어/"
headers = {"User-Agent": "Mozilla/5.0"}

for ch in initials:
    url = base_url + urllib.parse.quote(ch)
    print(f"📥 {ch} 페이지 크롤링 중: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"❌ {ch} 페이지 실패: {e}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    words = []

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
                    words.append(word)

    # 파일 경로: long_words/words_ㄱ.json 등
    filename = os.path.join(save_dir, f"words_{ch}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)

    print(f"✅ {ch}: {len(words)}개 단어 저장됨 → {filename}")

    time.sleep(1)  # 서버 보호를 위한 대기
