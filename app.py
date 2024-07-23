import streamlit as st
from g4f.client import Client
import time

# Đọc nội dung từ hai file
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()

file_content_1 = read_file('cau_hoi_thuong_gap.txt')
file_content_2 = read_file('thong_tin_tuyen_sinh.txt')

def stream_data(data):
     for word in data.split():
        yield word + " "
        time.sleep(0.04)

# Kết hợp nội dung của cả hai file
combined_content = f"Nội dung từ file câu hỏi thường gặp:\n\n{file_content_1}\n\nNội dung từ file thông tin tuyển sinh:\n\n{file_content_2}"

# Tạo hàm để gọi API GPT-3.5-turbo
def get_response(prompt):
    client = Client()
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    response = ""
    for completion in chat_completion:
        response += completion.choices[0].delta.content or ""
    return response

# Khởi tạo session state để lưu lịch sử chat
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Giao diện người dùng với Streamlit
st.set_page_config(page_title="AI Tư vấn tuyển sinh", page_icon=":books:")
st.header("AI Tư vấn tuyển sinh :books:")

st.write("Dựa trên dữ liệu từ các file, hãy nhập câu hỏi của bạn:")

# Thêm input để người dùng nhập câu hỏi
user_question = st.text_input("Nhập câu hỏi của bạn:")

if st.button("Đặt câu hỏi"):
    if user_question:
        prompt = f"Dựa trên dữ liệu sau đây:\n\n{combined_content}\n\nHãy trả lời câu hỏi: {user_question}"
        response = get_response(prompt)
        
        # Lưu câu hỏi và câu trả lời vào lịch sử chat
        st.session_state.chat_history.append(("User", user_question))
        st.session_state.chat_history.append(("Assistant", response))
        
        # Hiển thị câu trả lời
        st.write(stream_data(response))
        # Xóa câu hỏi sau khi đã nhận câu trả lời
        st.session_state.user_question = ""
    else:
        st.write("Vui lòng nhập câu hỏi trước khi nhấn nút nhận phản hồi.")

# Hiển thị lịch sử chat
st.subheader("Lịch sử chat")
chat_container = st.container()

with chat_container:
    for idx, (role, message) in enumerate(st.session_state.chat_history):
        if role == "User":
            st.text_input("Bạn:", value=message, key=f"user_{idx}", disabled=True)
        else:
            st.text_area("Assistant:", value=message, key=f"assistant_{idx}", disabled=True)