#챗GPT & 파이썬으로 AI 직원 만들기  

-프로그램 기획-
1. 챗 GPT를 이용하여 사용자가 원하는 음악을 찾기
2. 선곡한 음악의 음원 파일을 찾아서 다운
3. 음익과 관련된 이미지 생성
4. 음원과 이미지를 편집하여 영상 제작
5. 영상에 음악과 관련된 정보를 삽입

IDE : vscode  
사용 언어 : Python 3.12.1  
가상 환경 만들기 : python -m venv venv   
챗 GPT API 키 발급 : https://platform.openai.com/api-keys  

-개발 중 이슈 생길 때마다 업데이트-
1. API 키 환경 변수에 설정하여 숨기기(윈도우 10 파워쉘에서.)
```powershell
$env:OPENAI_API_KEY='api_key넣기'
```
2. 환경 설정에서 설정  
변수 이름 : OPENAI_API_KEY  
변수 값 : API_KEY 값  
3. 출력 값에서 한글이 깨질 때
```py
import sys

# Set the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')
```