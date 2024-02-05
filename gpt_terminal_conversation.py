import openai #OpenAI API를 사용
import os
import sys

# Set the encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

openai.api_key = os.getenv("OPENAI_API_KEY", default="") #API 키를 환경 변수에 저장하고 불러온다.

#OpenAI 챗봇 모델에 메시즈를 보내고 응답하는 함수
def send_message(message_log): 
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        max_tokens=1000, #생성된 응답에서 최대 토큰 수 설정
        messages = message_log,
        temperature=0.5, #생성된 응답의 창의성 올림
    )

    #텍스트가 포함된 챗봇의 첫 번째 응답 찾기(일부 응답에는 텍스트가 없을 수 있음)
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message['content'] 
    
def main():
    #챗봇에서 받은 메시지로 대화 기록 초기화 하기
    message_log = [
        {"role":"system", "content":"you are a helpful assistant."}, # system은 사용자를 도와주는 도우미로 설정
    ]

    #'quit'를 입력할 때까지 실행되는 루프 시작하기
    while True:
        #터미널에서 사용자의 입력 받기
        user_input = input("You: ")

        #사용자가 'quit'를 입력하면 루프를 종료하고 작별 메시지 출력하기
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        #사용자의 입력을 대화 기록에 추가하기
        message_log.append({"role": "user", "content": user_input})

        #챗봇에게 대화 기록을 보내 응답받기
        response = send_message(message_log)

        #대화 기록에 챗봇의 응답을 추가하고 콘솔에 출력하기
        message_log.append({"role": "assistant", "content": response})
        print(f"assistant: {response}")

if __name__ == "__main__":
    main()



