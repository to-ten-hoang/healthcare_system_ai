from flask import Flask, request, render_template
import pandas as pd
import joblib
from googletrans import Translator
import httpx
import numpy as np
import asyncio

app = Flask(__name__)

# Tải mô hình và MultiLabelBinarizer
model = joblib.load('D:/Study/Semester_2_2024_2025/SOFTWARE_ARCHITECTURE_DESIGN/the_end/disease_model.pkl')
mlb = joblib.load('D:/Study/Semester_2_2024_2025/SOFTWARE_ARCHITECTURE_DESIGN/the_end/mlb.pkl')

# Danh sách từ vựng
symptom_translation = {
    'ngứa': ' itching',
    'phát ban da': ' skin_rash',
    'sốt': ' high_fever',
    'ho': ' cough',
    'đau bụng': ' abdominal_pain',
    'mệt mỏi': ' fatigue',
    'buồn nôn': ' nausea',
    'hắt hơi liên tục': ' continuous_sneezing',
    'run rẩy': ' shivering',
    'ớn lạnh': ' chills',
    'chảy nước mắt': ' watering_from_eyes',
    'đau dạ dày': ' stomach_pain',
    'đau ngực': ' chest_pain',
    'đau khớp': ' joint_pain',
    'đau đầu': ' headache',
    'tiêu chảy': ' diarrhoea',
    'táo bón': ' constipation',
    'chóng mặt': ' dizziness',
    'nôn mửa': ' vomiting',
    'sưng hạch bạch huyết': ' swelled_lymph_nodes',
}

# Ánh xạ bệnh sang tiếng Việt
disease_translation = {
    'Fungal infection': 'Nhiễm trùng nấm',
    'Bronchial Asthma': 'Hen suyễn phế quản',
    'Common Cold': 'Cảm lạnh thông thường',
    'Pneumonia': 'Viêm phổi',
    'Allergy': 'Dị ứng',
    'Peptic ulcer diseae': 'Bệnh loét dạ dày',
    'Alcoholic hepatitis': 'Viêm gan do rượu',
    'Chronic cholestasis': 'Xơ gan mãn tính',
}

async def translate_text(text, src='en', dest='vi'):
    translator = Translator(timeout=httpx.Timeout(10.0))
    result = await translator.translate(text, src=src, dest=dest)
    return result.text

def translate_symptoms(vietnamese_symptoms):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    translator = Translator(timeout=httpx.Timeout(10.0))
    english_symptoms = []
    for symptom in vietnamese_symptoms:
        if symptom in symptom_translation:
            english_symptoms.append(symptom_translation[symptom])
        else:
            try:
                translated = loop.run_until_complete(translate_text(symptom, src='vi', dest='en'))
                translated = ' ' + translated.lower().replace(' ', '_')
                english_symptoms.append(translated)
            except Exception as e:
                print(f"Không thể dịch '{symptom}': {e}")
                continue
    loop.close()
    return english_symptoms

def predict_disease(vietnamese_symptoms):
    english_symptoms = translate_symptoms(vietnamese_symptoms)
    
    valid_symptoms = [s for s in english_symptoms if s in mlb.classes_]
    if not valid_symptoms:
        return "Lỗi: Không có triệu chứng hợp lệ để dự đoán.", "", []
    
    symptoms_vector = mlb.transform([valid_symptoms])
    
    # Dự đoán và lấy xác suất
    prediction = model.predict(symptoms_vector)[0]
    probabilities = model.predict_proba(symptoms_vector)[0]
    top_3_indices = np.argsort(probabilities)[-3:][::-1]
    top_3_diseases = [model.classes_[i] for i in top_3_indices]
    top_3_probs = [probabilities[i] for i in top_3_indices]
    top_3_results = [(disease, prob) for disease, prob in zip(top_3_diseases, top_3_probs)]
    
    # Dịch bệnh sang tiếng Việt
    if prediction in disease_translation:
        vietnamese_disease = disease_translation[prediction]
    else:
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            vietnamese_disease = loop.run_until_complete(translate_text(prediction, src='en', dest='vi'))
            loop.close()
        except Exception as e:
            print(f"Không thể dịch bệnh '{prediction}': {e}")
            vietnamese_disease = prediction
    
    return vietnamese_disease, prediction, top_3_results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symptoms = request.form['symptoms'].split(',')
        symptoms = [s.strip() for s in symptoms]
        viet_disease, eng_disease, top_3 = predict_disease(symptoms)
        # Chuẩn bị dữ liệu top 3 để hiển thị
        top_3_formatted = [
            (disease_translation.get(disease, disease), f"{prob:.2f}")
            for disease, prob in top_3
        ]
        return render_template('index.html', prediction=viet_disease, english_prediction=eng_disease, top_3=top_3_formatted)
    return render_template('index.html', prediction=None, english_prediction=None, top_3=None)

if __name__ == '__main__':
    app.run(debug=True)