import os
import sys
sys.stdout.reconfigure(encoding='utf-8')# UTF-8 인코딩 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../') #config 파일 경로
from config import OPENAI_API_KEY #프로젝트 내에 config 파일에 api_key를 설정
from openai import OpenAI # openai==1.1.1 설정

#프로젝트 내에 config 파일에 api_key를 설정 했을 때
client = OpenAI(api_key=OPENAI_API_KEY)

def ask_to_gpt_35_turbo(user_input): #사용자가 입력한 질문인 user_input 인자를 받는다.
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        top_p=0.1, #모델이 생성한 텍스트 중에서 가장 확율이 높은 텍스트를 선택
        temperature=0.1, #모델이 다음 단어를 예츨할 때 무작위성을 추가 하기 위해 사용
        messages=[
            {"role":"system", "content":"you are a helpful assistant."}, # system은 사용자를 도와주는 도우미로 설정
            {"role":"user", "content": user_input} #user 역살로 사용
        ]
    )

    if response.choices and response.choices[0].message:
        return response.choices[0].message.content #답변중 첫번째 답변을 반환
    else:
        return "Error: Empty response from the OpenAI model."

#유니코드 문자열 출력을 위해 u 접두사 사용
user_request=u''' 
최근 가장 인기 있는 프로그램 언어를 비교해 줘.
'''
r=ask_to_gpt_35_turbo(user_request)
print(r)
