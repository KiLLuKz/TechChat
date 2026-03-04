import os
from flask import Flask, request, jsonify
from google import genai  # ใช้แบบใหม่

app = Flask(__name__)

# ตั้งค่า Client ของ Gemini รุ่นใหม่
client = genai.Client(api_key=os.environ.get('GEMINI_KEY'))

@app.route('/')
def home():
    return "AI Bot is Online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_query = req.get('queryResult').get('queryText')

    try:
        # วิธีเรียกใช้งาน Gemini แบบใหม่ล่าสุด
        response = client.models.generate_content(
            model="gemini-2.0-flash", # หรือรุ่นที่คุณต้องการใช้
            contents=f"คุณคือ AI เพื่อนซี้ที่คุยสนุก ตอบคำถามนี้เป็นภาษาไทย: {user_query}"
        )
        reply = response.text
    except Exception as e:
        # บรรทัดนี้จะช่วยให้เรารู้ว่า Error จริงๆ คืออะไรในหน้า Log
        print(f"Detailed Error: {e}")
        reply = "ขอโทษทีนะ เรามึนๆ นิดหน่อย ลองอีกทีนะ!"

    return jsonify({"fulfillmentText": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
