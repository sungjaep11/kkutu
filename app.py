from flask import Flask, render_template, request
import os
import json
from collections import Counter

app = Flask(__name__)

# 파일 경로 설정
LONG_WORDS_DIR = "long_words"
ATK_WORDS_FILE = "atk_words_combined.json"
MISSION_WORDS_FILE = "mission_words.json"

# JSON 로드 함수
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# 초성 추출 함수
def get_initial(ch):
    initial_base = 44032  # '가'
    ch_code = ord(ch)
    if not (0xAC00 <= ch_code <= 0xD7A3):
        return ch  # ㄱ, ㄴ 등 초성 직접 입력 시
    chosung_index = (ch_code - initial_base) // (21 * 28)
    return "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"[chosung_index]

@app.route("/", methods=["GET", "POST"])
def index():
    query = request.form.get("query", "").strip()
    left_results = []
    right_results = []

    if len(query) == 1:
        # 1글자 입력: 긴 단어 + 공격 단어

        # 긴 단어 처리
        initial = get_initial(query)
        long_words_path = os.path.join(LONG_WORDS_DIR, f"words_{initial}.json")
        if os.path.exists(long_words_path):
            long_words = load_json(long_words_path)
            left_results = [w for w in long_words if w.startswith(query)]

        # 공격 단어 처리 (길이 긴 순으로 정렬)
        atk_words = load_json(ATK_WORDS_FILE)
        filtered_atk = [w for w in atk_words if w.startswith(query)]
        right_results = sorted(filtered_atk, key=lambda w: -len(w))

    elif len(query) == 2:
        # 2글자 입력
        mission_words = load_json(MISSION_WORDS_FILE)
        filtered = [w for w in mission_words if w.startswith(query[0]) and query[1] in w[1:]]

        # 두 번째 글자 빈도 많은 순 → 길이 긴 순
        def sort_key(word):
            freq = word[1:].count(query[1])
            return (-freq, -len(word))

        right_results = sorted(filtered, key=sort_key)

        if not right_results:
            initial = get_initial(query[0])
            long_words_path = os.path.join(LONG_WORDS_DIR, f"words_{initial}.json")
            if os.path.exists(long_words_path):
                long_words = load_json(long_words_path)
                left_results = [w for w in long_words if w.startswith(query[0])]

            atk_words = load_json(ATK_WORDS_FILE)
            filtered_atk = [w for w in atk_words if w.startswith(query[0])]
            right_results = sorted(filtered_atk, key=lambda w: -len(w))

    return render_template("index.html",
                           query="",
                           left_results=left_results,
                           right_results=right_results)

if __name__ == "__main__":
    app.run(debug=True)
