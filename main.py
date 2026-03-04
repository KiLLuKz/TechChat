import os
from flask import Flask, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# ดึง Key จากระบบ Render
genai.configure(api_key=os.environ.get('GEMINI_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return "AI Bot is Online!"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    user_query = req.get('queryResult').get('queryText')

    # ส่งให้ Gemini ตอบแบบ Small Talk
    prompt = f"คุณคือ AI เพื่อนซี้ที่คุยสนุกและกวนนิดๆ ตอบคำถามนี้เป็นภาษาไทย: {user_query}"
    
    try:
        response = model.generate_content(prompt)
        reply = response.text
    except:
        reply = "มึนตึ้บเลย ขออีกทีได้ป่าว"

    return jsonify({"fulfillmentText": reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
