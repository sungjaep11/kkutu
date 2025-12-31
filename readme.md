# 끄투 한국어 단어 검색기 🔍

이 프로젝트는 끄투(KKUTO) 게임을 위한 한국어 단어 검색 도구입니다.  
한글 초성 또는 글자 조합을 입력하면, 미리 수집된 단어 DB를 기반으로 검색 결과를 보여줍니다.

## 주요 기능

- `가`같은 1글자 입력 시:
  - 왼쪽: 긴 단어 (long_words)
  - 오른쪽: 공격 단어 (atk_words)

- `가사`처럼 2글자 입력 시:
  - 미션 단어 (mission_words) 검색

## 업데이트 방법

- scrape_long.py 실행 -> 긴단어를 /long_words 폴더에 저장
- scrape_mission.py 실행 -> 미션단어를 mission_words.json에 저장
- scrape_atk.py 실행 -> 공격단어(끄코)를 atk_words_kkuko.json에 저장
- 나무위키 공격단어를 텍스트 파일로 복붙해 ai를 이용해 atk_words_namu.json로 변환
- 챗지피티로 atk_words_combined.json로 공격단어 통합

