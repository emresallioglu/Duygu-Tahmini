from flask import Flask, request, render_template
import xml.etree.ElementTree as ET
import pandas as pd
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# NLTK Türkçe durak sözcüklerini indir
import nltk

nltk.download('stopwords')
nltk.download('punkt')

# Türkçe durak sözcükler
stop_words = set(stopwords.words('turkish'))


def temizle(text):
    # Küçük harfe dönüştür
    text = text.lower()
    # Noktalama işaretlerini kaldır
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Sayıları kaldır
    text = re.sub(r'\d+', '', text)
    # Durak sözcükleri kaldır
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    # Temizlenmiş metni tekrar birleştir
    return ' '.join(tokens)


# Flask uygulamasını başlat
app = Flask(__name__)

# XML dosyasını oku
tree = ET.parse('TREMODATA.xml')
root = tree.getroot()

# Verileri saklamak için listeler oluştur
entries = []
original_emotions = []
validated_emotions = []

# Duyguları çevirmek için bir sözlük oluştur
emotion_translation = {
    'Anger': 'Öfke',
    'Disgust': 'Tiksinti',
    'Fear': 'Korku',
    'Happy': 'Mutlu',
    'Sadness': 'Üzgün',
    'Surprise': 'Şaşkınlık'
}

# Bilinmeyen etiketler için varsayılan değer
default_emotion = 'Belirsiz'

# XML verisini ayrıştır
for doc in root.findall('Doc'):
    entry = doc.find('Entry').text
    original_emotion = doc.find('OriginalEmotion').text
    validated_emotion = doc.find('ValidatedEmotion').text

    # Orijinal duyguyu çevir
    original_emotion_translated = emotion_translation.get(original_emotion, default_emotion)
    if original_emotion_translated == default_emotion:
        print(f'Uyarı: Bilinmeyen orijinal duygu etiketi "{original_emotion}" bulundu.')

    # Doğrulanmış duyguyu çevir
    validated_emotion_translated = emotion_translation.get(validated_emotion, default_emotion)
    if validated_emotion_translated == default_emotion:
        print(f'Uyarı: Bilinmeyen doğrulanmış duygu etiketi "{validated_emotion}" bulundu.')

    entries.append(entry)
    original_emotions.append(original_emotion_translated)
    validated_emotions.append(validated_emotion_translated)

# Verileri DataFrame'e dönüştür
data = pd.DataFrame({
    'Entry': entries,
    'OriginalEmotion': original_emotions,
    'ValidatedEmotion': validated_emotions
})

# Veriyi temizleme
data['CleanedEntry'] = data['Entry'].apply(temizle)

# TF-IDF vektörleştirici
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(data['CleanedEntry'])

# Veriyi eğitim ve test setlerine ayırma
X_train, X_test, y_train, y_test = train_test_split(X, data['ValidatedEmotion'], test_size=0.2, random_state=42)

# Lojistik regresyon modeli
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


# Tahmin fonksiyonu
def tahmin_et(cumle):
    cumle = temizle(cumle)
    vektor = vectorizer.transform([cumle])
    olasiliklar = model.predict_proba(vektor)[0]
    duygular = model.classes_
    duygular_ve_olasiliklar = sorted(zip(duygular, olasiliklar), key=lambda x: x[1], reverse=True)
    return duygular_ve_olasiliklar


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/tahmin', methods=['POST'])
def tahmin():
    cumle = request.form['cumle']
    tahminler = tahmin_et(cumle)
    return render_template('result.html', cumle=cumle, tahminler=tahminler)


if __name__ == '__main__':
    app.run(debug=True)
