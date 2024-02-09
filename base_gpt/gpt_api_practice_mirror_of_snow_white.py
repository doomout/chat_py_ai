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
        top_p=0.1, 
        temperature=0.1, 
        messages=[
            {"role":"system", "content":"You are the mirror of Snow White. You must pretend like the mirror of the story."}, # system를 백설공주의 거울로 설정
            {"role":"user", "content": user_input} 
        ]
    )

    if response.choices and response.choices[0].message:
        return response.choices[0].message.content #답변중 첫번째 답변을 반환
    else:
        return "Error: Empty response from the OpenAI model."

#유니코드 문자열 출력을 위해 u 접두사 사용
user_request=u''' 
거울아! 거울아! 세상에서 누가 제일 이쁘니?
'''
r=ask_to_gpt_35_turbo(user_request)
print(r)
