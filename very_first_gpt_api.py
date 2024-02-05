import openai #OpenAI API를 사용
import os

openai.api_key = os.getenv("OPENAI_API_KEY", default="") #API 키를 환경 변수에 저장하고 불러온다.

def ask_to_gpt_35_turbo(user_input): #사용자가 입력한 질문인 user_input 인자를 받는다.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        top_p=0.1, #모델이 생성한 텍스트 중에서 가장 확율이 높은 텍스트를 선택
        temperature=0.1, #모델이 다음 단어를 예츨할 때 무작위성을 추가 하기 위해 사용
        messages=[
            {"role":"system", "content":"you are a helpful assistant."}, # system은 사용자를 도와주는 도우미로 설정
            {"role":"user", "content": user_input} #user 역살로 사용
        ]
    )

    if response.choices and response.choices[0].message:
        return response.choices[0].message['content'] #답변중 첫번째 답변을 반환
    else:
        return "Error: Empty response from the OpenAI model."
    #return response.choices[0].message['content'] #답변중 첫번째 답변을 반환

#유니코드 문자열 출력을 위해 u 접두사 사용
user_request=u''' 
최근 가장 인기 있는 프로그램 언어를 비교해 줘.
'''
r=ask_to_gpt_35_turbo(user_request)
print(r)
