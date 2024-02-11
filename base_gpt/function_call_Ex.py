from openai import OpenAI
import json
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')# UTF-8 인코딩 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../') #config 파일 경로
from config import OPENAI_API_KEY #프로젝트 내에 config 파일에 api_key를 설정

client = OpenAI(api_key=OPENAI_API_KEY)

#현재 날씨를 가져오는 함수
def get_current_weather(location, unit="fahrenheit"):
    """location 으로 받은 지역의 날씨를 알려주는 기능"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

# 대화 실행 함수
def run_conversation():
    # 1단계: 대화 및 사용 가능한 함수를 모델에게 전송합니다.
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=messages,
        tools=tools,
        tool_choice="auto",  #auto가 기본 설정
    )
    response_message = response.choices[0].message

    tool_calls = response_message.tool_calls
     # 2단계: 모델이 함수를 호출할지 확인합니다.
    if tool_calls:
        # 3단계: 함수를 호출합니다.
        available_functions = {
            "get_current_weather": get_current_weather,
        }  
        messages.append(response_message) 

        # 4단계: 각 함수 호출 및 함수 응답 정보를 모델에게 전송합니다.
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  
        second_response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=messages,
        )  #함수 실행 결과를 GPT에 보내 새로운 답변 받아오기
        return second_response
print(run_conversation())