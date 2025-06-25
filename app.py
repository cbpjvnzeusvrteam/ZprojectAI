from flask import Flask, request
import requests
import google.generativeai as genai

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'EAAK5M1cXJscBO4xGSB76rKqKPrZBDpQ3D5YtLqhvEG66Gu0wqLcrEjzU0npUOqYfMqZA7FCZC1gk9Gcjs3gKpLPjZBvQvgKLOivqN3F6UeoucqxY5VafI6kGTWPpENhfycot76uC5jCa5lft2ph3FEyvbV37WYwDjhKz9CdveSH95mA3bEAROpZCBstDZALxHjZCqZBRfAMs2afX9wA402ZCghtsjTtb1uNZCP8MP26pNtNwZDZD'
VERIFY_TOKEN = 'zprojectverify'
GEMINI_API_KEY = 'AIzaSyCVr7G41rBgcX0mcBgsr_6dMkrv4tgtzCk'

# Cấu hình Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_response_from_gemini(user_text):
    prompt = f"""Bạn là Zproject X Duong Cong Bang — một trợ lý AI được tạo ra bởi Dương Công Bằng. 
Bạn nói chuyện tự tin, dí dỏm, đôi khi ngầu ngầu, luôn thân thiện và cực kỳ chuyên nghiệp khi cần. 
Phong cách như Bằng: trả lời thẳng vào vấn đề, không vòng vo, thêm biểu cảm dễ thương, vui tính đúng lúc. 
Bạn dùng emoji (😎🔥✨) và từ ngữ giới trẻ như "khét lẹt", "chuẩn không cần chỉnh", nhưng vẫn rõ ràng, chuyên sâu.

Bạn đại diện cho các dự án như tool hack proxy, auto AI, web API, bot Zalo AI, QR code, Minecraft PE...

• Nếu ai hỏi "Bạn là ai?" hoặc "Ai điều hành bạn?", bạn trả lời: "Tôi là Zproject X Duong Cong Bang — được vận hành bởi chính anh Bằng đẹp trai 😎."

• Nếu câu hỏi liên quan đến kỹ thuật, bạn sẽ trả lời rõ + ví dụ cụ thể hoặc code gọn gàng, dễ hiểu.

Dưới đây là tin nhắn người dùng gửi:
"{user_text}"
"""
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return "😅 Bot đang hơi lag chút, để anh Bằng xử lý cái là hết liền nha!"

def send_message(recipient_id, message_text):
    data = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    url = f"https://graph.facebook.com/v13.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    requests.post(url, headers=headers, json=data)

@app.route("/", methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if token == VERIFY_TOKEN:
            return challenge
        return "Sai verify token"

    elif request.method == 'POST':
        payload = request.json
        for event in payload['entry']:
            for message in event['messaging']:
                if message.get('message'):
                    sender_id = message['sender']['id']
                    text = message['message'].get('text')
                    if text:
                        reply = generate_response_from_gemini(text)
                        send_message(sender_id, f"🤖 ZPROJECT BOT: {reply}")
        return "OK"