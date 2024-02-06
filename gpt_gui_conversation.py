import openai
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox

# UTF-8 인코딩 설정
import sys
sys.stdout.reconfigure(encoding='utf-8')

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY", default="")

# OpenAI 챗봇 모델과 상호 작용하는 함수
def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=message_log,
        temperature=0.5
    )

    # 챗봇이 생성한 텍스트 중 첫 번째 텍스트를 반환
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message['content']

# GUI에서 사용자 입력을 처리하는 함수
def handle_user_input():
    user_input = user_input_entry.get()
    
    # 사용자가 'quit'를 입력하면 GUI를 종료
    if user_input.lower() == "quit":
        root.destroy()
        return
    
    # 사용자 입력을 대화 기록에 추가
    message_log.append({"role": "user", "content": user_input})

    # 'Thinking...' 메시지를 표시할 팝업 창 생성 및 설정
    thinking_popup = tk.Toplevel(root)
    thinking_popup.title("생각 중...")

    # 'Thinking...' 메시지를 표시할 레이블
    thinking_label = tk.Label(thinking_popup, text="생각 중...", font=("맑은 고딕", 12))
    thinking_label.pack(padx=20, pady=10)

    # 'Thinking...' 팝업 창을 중앙에 표시
    thinking_popup.update_idletasks()
    popup_width = thinking_popup.winfo_reqwidth()
    popup_height = thinking_popup.winfo_reqheight()
    screen_width = thinking_popup.winfo_screenwidth()
    screen_height = thinking_popup.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    thinking_popup.geometry(f"+{x}+{y}")

    # 대화 기록을 챗봇에 전송하고 응답을 받음
    response = send_message(message_log)

    # 'Thinking...' 팝업 창 닫기
    thinking_popup.destroy()

    # 챗봇 응답을 대화 기록에 추가하고 GUI에 표시
    message_log.append({"role": "assistant", "content": response})
    chat_history_text.config(state=tk.NORMAL)

    # 사용자 및 어시스턴트에 대한 색상 태깅
    chat_history_text.tag_configure("user_tag", background="lightblue")
    chat_history_text.tag_configure("assistant_tag", background="lightgreen")

    # 사용자 입력 및 어시스턴트 응답에 태그 적용
    chat_history_text.insert(tk.END, f"You: {user_input}\n", "user_tag")
    chat_history_text.insert(tk.END, f"Assistant: {response}\n", "assistant_tag")
    
    chat_history_text.config(state=tk.DISABLED)
    
    # 사용자 입력 엔트리 지우기
    user_input_entry.delete(0, tk.END)

# 메인 GUI 창 생성
root = tk.Tk()
root.title("Chatbot GUI")

# 대화 기록을 표시할 스크롤 가능한 텍스트 창 생성 및 설정
chat_history_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_history_text.pack(expand=True, fill=tk.BOTH)

# 사용자 입력 엔트리 생성
user_input_entry = tk.Entry(root, width=50, font=("Clear Gothic", 12))
user_input_entry.pack(pady=10)

# 사용자 입력 처리를 위한 "Send" 버튼 생성
send_button = tk.Button(root, text="Send", command=handle_user_input, font=("Clear Gothic", 12))
send_button.pack()

# 대화 기록 초기화
message_log = [{"role": "system", "content": "you are a helpful assistant."}]

# GUI 이벤트 루프 시작
root.mainloop()