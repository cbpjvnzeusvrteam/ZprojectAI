from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

GEMINI_API_KEY = "AIzaSyA2y3gaSFOfiRHpmH2CK3KL-7YqV-75xSM"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_response(user_text):
    headers = {
        "Content-Type": "application/json"
    }

    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"""Bạn là Zproject X Duong Cong Bang — AI do anh Bằng đẹp trai tạo ra 😎.

Phong cách: trả lời nhanh, gọn, khét lẹt, đôi khi chèn emoji như 🔥✨ nhưng vẫn chính xác. Ai hỏi kỹ thuật thì trả lời cụ thể + ví dụ code nếu được.

Người dùng vừa hỏi:
{user_text}
"""
                    }
                ]
            }
        ]
    }

    try:
        res = requests.post(GEMINI_API_URL, headers=headers, json=body)
        res_json = res.json()

        # In log ra terminal Render
        print("📥 Gemini response JSON:", res_json)

        # Lấy nội dung trả lời
        return res_json['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception as e:
        print("❌ Lỗi xảy ra:", e)
        return f"❌ Lỗi hệ thống: {str(e)}"
        
@app.route("/ask", methods=["GET"])
def ask():
    cauhoi = request.args.get("cauhoi")
    if not cauhoi:
        return jsonify({"error": "Thiếu tham số 'cauhoi'"}), 400

    reply = generate_response(cauhoi)
    return jsonify({"response": reply})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)