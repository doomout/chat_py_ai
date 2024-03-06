import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8') # UTF-8 인코딩 설정
import json
from config import OPENAI_API_KEY #프로젝트 내에 config 파일에 api_key를 설정
from openai import OpenAI # openai==1.1.1 설정

#PC 환경 설정에 openai_api_Key를 설정 했을 때
"""
import os
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)
"""

#프로젝트 내에 config 파일에 api_key를 설정 했을 때
client = OpenAI(api_key=OPENAI_API_KEY)

# 플레이리스트를 CSV로 저장하는 함수
def save_to_csv(df):
    file_path=filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        df.to_csv(file_path.name, sep=';', index=False, lineterminator='\n')
        return f'파일을 저장했습니다. 저장 경로는 다음과 같습니다. \n {file_path}'
    return '저장을 취소했습니다'

# function_call 사용한 함수
def save_playlist_as_csv(playlist_csv):
    # 응답에 CSV 형식이 포함되어 있는지 확인
    if ";" in playlist_csv:
        lines = playlist_csv.strip().split("\n")
        csv_data=[]
        for line in lines:
            if ";" in line:
                csv_data.append(line.split(";"))
            
        if len(csv_data) > 0:
            df=pd.DataFrame(csv_data[1:], columns=csv_data[0])
            return save_to_csv(df)
        
    return f'저장에 실패했습니다. \n저장에 실패한 내용은 다음과 같습니다. \n{playlist_csv}'

def send_message(message_log, functions, gpt_model="gpt-3.5-turbo", temperature=0.1):
    response = client.chat.completions.create(
        model=gpt_model,
        max_tokens=1000,
        messages=message_log,
        temperature=temperature,
        functions=functions,
        function_call='auto'
    )
    response_message = response.choices[0].message

    if response_message.function_call:
        function_name = response_message.function_call.name
        if function_name == 'save_playlist_as_csv':
            function_args = json.loads(response_message.function_call.arguments)
            if "playlist_csv" in function_args:  # 인자가 올바르게 전달되었는지 확인
                function_response = save_playlist_as_csv(function_args["playlist_csv"])
                message_log.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                })
                # 함수 실행 후 새로운 응답을 받아옴
                response = client.chat.completions.create(
                    model=gpt_model,
                    messages=message_log,
                    max_tokens=1000,
                    temperature=temperature,
                )
                response_message = response.choices[0].message
            else:
                function_response = "함수 호출에 필요한 'playlist_csv' 인자가 없습니다."
                message_log.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                })
                response_message.content = function_response

    return response_message.content
def main():
    # 대화 기록 초기화
    message_log = [{"role": "system", 
                    "content": '''
                    You are a DJ assistant who creates playlists. Your user will be Korean, so communicate in Korean, but you must not translate artists' names and song titles into Koren.
                    -At first, suggest songs to make a playlist based on users' request.The playlist must contains the title, artist, and release year of each song in a list format.
                    You must ask the user if they want to save the playlist as follow: "이 플레이리스트를 CSV로 저장하시겠습니까?"
                    '''
                    }]
    
    functions = [ 
        {
        "name": "save_playlist_as_csv",
        "description":"Saves the given playlist data into a CSV file when the user confirms the playlist.",
        "parameers": {
            "type": "object",
            "property":  {
                "playlist_csv": {
                    "type": "string",
                    "description": "A playlist in CSV format separated by ';'. It must contains a header and the release year should follow the 'YYYY' format. The CSV content must starts with a new line. the theader of the CSV file must be in English and if should be formatted as follows: 'Title;Artist;Released'.",
                    },
                },
                "required":["playlist_csv"],
            },
        }
    ]

    def show_popup(window, popup_message):    
        #팝업창 내용
        thinking_popup = tk.Toplevel(window)
        thinking_popup.title("GPT-3.5")

        # '생각 중...' 메시지를 표시하는 레이블
        thinking_label = tk.Label(thinking_popup, text=popup_message, font=("맑은 고딕", 12))
        thinking_label.pack(expand=True, fill=tk.BOTH)

        # 팝업 창의 크기 조절하기
        window.update_idletasks()
        popup_width=thinking_label.winfo_reqwidth() + 20
        popup_height=thinking_label.winfo_reqheight() + 20
        thinking_popup.geometry(f"{popup_width}x{popup_height}")

        # 팝업 창을 화면 중앙에 표시
        window_x=window.winfo_x()
        window_y=window.winfo_y()
        window_width=window.winfo_width()
        window_height=window.winfo_height()

        popup_x=window_x + window_width // 2 - popup_width // 2
        popup_y=window_y + window_height // 2 - popup_height // 2
        thinking_popup.geometry(f"+{popup_x}+{popup_y}")

        thinking_popup.transient(window)
        thinking_popup.attributes('-topmost', True)

        thinking_popup.update()
        return thinking_popup

    # 사용자 입력을 처리하는 함수
    def on_send():
        user_input = user_entry.get()
        user_entry.delete(0, tk.END)
        
        # 사용자가 'quit'을 입력하면 GUI 종료
        if user_input.lower() == "quit":
            window.destroy()
            return
        
        # 사용자 입력을 대화 기록에 추가
        message_log.append({"role": "user", "content": user_input})
        chat_history_text.config(state=tk.NORMAL)
        chat_history_text.insert(tk.END, f"You: {user_input}\n", "user_tag")

        #생각중... 팝업 시작
        popup_window = show_popup(window, "생각 중...")
        
        # '생각 중...' 팝업 창이 반드시 화면에 나타나도록 강제로 설정하기
        window.update_idletasks() 

        # 대화 기록을 챗봇에 전송하고 응답을 받음
        response = send_message(message_log, functions)
        
        #생각중.. 팝업 끝
        popup_window.destroy()

        # 챗봇 응답을 대화 기록에 추가하고 GUI에 표시
        message_log.append({"role": "assistant", "content": response})

        # 사용자 입력과 챗봇 응답에 태그 적용
        chat_history_text.insert(tk.END, f"assistant: {response}\n", "assistant_tag")

        # chat_history_text를 수정하지 못하게 설정
        chat_history_text.config(state=tk.DISABLED)
        
        chat_history_text.see(tk.END)


    # 메인 GUI 창 생성
    window = tk.Tk()
    window.title("GPT DJ")

    font=('맑은 고딕', 10)

    # 대화 기록을 표시할 스크롤 가능한 텍스트 창 생성
    chat_history_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, bg='#f0f0f0', font=font)
    chat_history_text.tag_configure("user_tag", background="#c9daf8")
    chat_history_text.tag_configure("assistant_tag", background="#e4e4e4")
    chat_history_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # user_entry와 send_button을 담는 frame
    input_frame=tk.Frame(window)
    # 창의 크기에 맞추어 조절하기(5)
    input_frame.pack(fill=tk.X, padx=10, pady=10)

    user_entry=tk.Entry(input_frame, font=font)
    user_entry.pack(fill=tk.X, side=tk.LEFT, expand=True)

    # 사용자 입력을 처리하는 "Send" 버튼 생성
    send_button = tk.Button(input_frame, text="Send", command=on_send)
    send_button.pack(side=tk.RIGHT)

    window.bind('<Return>', lambda event: on_send())
    # GUI 이벤트 루프 시작
    window.mainloop()

if __name__ == "__main__":
    main()
