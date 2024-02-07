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
0. openai 라이브러리 설치
```py
pip install openai
```
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
4. pandas 설치
```py
pip install pandas
```
5. pandas 란?  
Pandas는 파이썬 프로그래밍 언어를 위한 데이터 조작 및 분석 라이브러리
주로 표 형태의 데이터를 처리하고 조작하는 데 사용  
Pandas는 데이터 구조와 데이터 조작 도구를 제공하여 데이터를 쉽게 읽고, 쓰고, 변환하며, 분석할 수 있도록 도와줌  
- DataFrame: 행과 열로 구성된 표 형태의 데이터 구조를 제공합니다. 이는 스프레드시트나 SQL의 테이블과 유사한 형태로 데이터를 저장하고 조작할 수 있습니다.
- Series: 단일 열의 데이터를 다루는 데 사용되는 1차원 배열 형태의 데이터 구조입니다.
- 데이터 조작: 데이터 필터링, 정렬, 그룹화, 결측값 처리 등 다양한 데이터 조작 작업을 수행할 수 있습니다.
- 데이터 입출력: 다양한 데이터 소스에서 데이터를 읽고 쓸 수 있습니다. CSV, Excel, SQL 데이터베이스, JSON 등 다양한 포맷을 지원합니다.
- 데이터 시각화: 데이터를 시각화하여 그래프나 차트로 표현할 수 있는 기능을 제공합니다.
Pandas는 데이터 과학 및 머신러닝 프로젝트에서 매우 유용하며, 데이터 전처리, 탐색적 데이터 분석(EDA), 통계 분석 등 다양한 작업에 활용됩니다.

6. pyarrow 설치
pandas 라이브러리가 다음 주요 릴리스(pandas 3.0)에서 pyarrow를 필수 종속성으로 사용할 것이라는 것이라는 경고에 설치  
pandas 3.0 버전부터는 더 나은 성능을 위해 Arrow 문자열 유형과 같은 
더 나은 데이터 유형을 사용하고 다른 라이브러리와의 상호 운용성을 향상시키기 위해 pyarrow가 필요
```py
pip install pyarrow
```