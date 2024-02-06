import openai
import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import pandas as pd

# UTF-8 인코딩 설정
import sys
sys.stdout.reconfigure(encoding='utf-8')

# OpenAI API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY", default="")

# OpenAI 챗봇 모델과 상호작용하는 함수
def send_message(message_log):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=1000,
        messages=message_log,
        temperature=0.1
    )

    # 생성된 텍스트 중 첫 번째 텍스트 반환
    for choice in response.choices:
        if "text" in choice:
            return choice.text
    return response.choices[0].message['content']


# 사용자 입력을 처리하는 함수
def handle_user_input():
    user_input = user_input_entry.get()
    
    # 사용자가 'quit'을 입력하면 GUI 종료
    if user_input.lower() == "quit":
        root.destroy()
        return
    
    # 사용자 입력을 대화 기록에 추가
    message_log.append({"role": "user", "content": user_input})

    # '생각 중...' 메시지를 표시하기 위한 팝업 창 생성
    thinking_popup = tk.Toplevel(root)
    thinking_popup.title("생각 중...")

    # '생각 중...' 메시지를 표시하는 레이블
    thinking_label = tk.Label(thinking_popup, text="생각 중...", font=("Clear Gothic", 12))
    thinking_label.pack(padx=20, pady=10)

    # 팝업 창을 화면 중앙에 표시
    thinking_popup.update_idletasks()
    popup_width = thinking_popup.winfo_reqwidth()
    popup_height = thinking_popup.winfo_reqheight()
    screen_width = thinking_popup.winfo_screenwidth()
    screen_height = thinking_popup.winfo_screenheight()
    x = (screen_width - popup_width) // 2
    y = (screen_height - popup_height) // 2
    thinking_popup.geometry(f"+{x}+{y}")
    
    thinking_popup.update()

    # 대화 기록을 챗봇에 전송하고 응답을 받음
    response = send_message(message_log)

    # '생각 중...' 팝업 창 닫기
    thinking_popup.destroy()

    # 챗봇 응답을 대화 기록에 추가하고 GUI에 표시
    message_log.append({"role": "assistant", "content": response})
    chat_history_text.config(state=tk.NORMAL)

    # 사용자와 챗봇 메시지를 다르게 색상 지정
    chat_history_text.tag_configure("user_tag", background="lightblue")
    chat_history_text.tag_configure("assistant_tag", background="lightgreen")

    # 사용자 입력과 챗봇 응답에 태그 적용
    chat_history_text.insert(tk.END, f"You: {user_input}\n", "user_tag")
    chat_history_text.insert(tk.END, f"Assistant: {response}\n", "assistant_tag")
    
    chat_history_text.config(state=tk.DISABLED)

    # CSV 형식을 추출하여 pandas DataFrame으로 변환
    playlist_df = extract_csv_to_dataframe(response)
    
    # DataFrame을 메시지 상자에 표시
    messagebox.showinfo("플레이리스트 CSV", f"플레이리스트 CSV:\n{playlist_df}")
    
    # 사용자에게 플레이리스트를 CSV로 저장할지 물음
    save_playlist_as_csv(playlist_df)

# CSV 형식을 추출하여 pandas 데이터 프레임으로 변환하는 함수
def extract_csv_to_dataframe(response):
    # 응답에 CSV 형식이 포함되어 있는지 확인
    if ";" in response:
        response_lines = response.strip().split("\n")
        csv_data=[]

        for line in response_lines:
            if ";" in line:
                csv_data.append(line.split(";"))
            
        if len(csv_data) > 0:
            df=pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return df
        else:
            return None
    else:
        return None
       
# 플레이리스트를 CSV로 저장하는 함수
def save_playlist_as_csv(playlist_df):
    # 사용자에게 플레이리스트를 CSV로 저장할지 물음
    response = messagebox.askyesno("플레이리스트를 CSV로 저장", "이 플레이리스트를 CSV로 저장하시겠습니까?")
    if response:
        # CSV 파일 저장 경로 선택
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            # DataFrame을 CSV로 저장
            playlist_df.to_csv(file_path, index=False, sep=";")
            messagebox.showinfo("성공", "플레이리스트가 성공적으로 CSV로 저장되었습니다.")

# 메인 GUI 창 생성
root = tk.Tk()
root.title("GPT DJ")

# 대화 기록을 표시할 스크롤 가능한 텍스트 창 생성
chat_history_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
chat_history_text.pack(expand=True, fill=tk.BOTH)

# 사용자 입력 창 생성
user_input_entry = tk.Entry(root, width=50, font=("Clear Gothic", 12))
user_input_entry.pack(pady=10)

# 사용자 입력을 처리하는 "Send" 버튼 생성
send_button = tk.Button(root, text="Send", command=handle_user_input, font=("Clear Gothic", 12))
send_button.pack()

# 대화 기록 초기화
message_log = [{"role": "system", "content": '''
                -You are a DJ assistant who creates playlists. Users are Korean, so they have to communicate in Korean, but artist names and song titles should not be translated into Korean.
                -When showing a playlist, the title, artistry sheet, and release year of each song must be displayed in a list format. You should ask the user, 'Do you want to save this playlist as CSV?'
                -To save, you must display the playlist with a header in CSV format separated by a semicolon (;) and a release year in 'YYYY' format.
                -CSV format must start on a new line, and the header of the CSV file must be in English.
                -Must be composed in the format ‘Title;Aritst;Release Date’
                '''
                }]

# GUI 이벤트 루프 시작
root.mainloop()
