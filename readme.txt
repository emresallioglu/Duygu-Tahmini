# Duygu Tahmini Projesi

Bu proje, Türkçe cümlelerden duygu tahmini yapmak için geliştirilmiş bir Flask web uygulamasıdır.

## Gereksinimler

Bu projeyi çalıştırmak için aşağıdaki yazılımlara ihtiyacınız vardır:

- Python 3.7+
- pip (Python paket yöneticisi)
- Git (isteğe bağlı, projeyi bir repository'den klonlamak için)

## Kurulum Adımları

1. **Proje dosyalarını klonlayın veya indirin**:
   
Git kullanarak projeyi klonlayabilirsiniz: 

	git clone https://github.com/emresallioglu/Duygu-Tahmini.git
	cd Duygu-Tahmini

Alternatif olarak, proje dosyalarını doğrudan indirebilir ve bir klasöre çıkartabilirsiniz.


2. **Sanal ortam oluşturun ve etkinleştirin**:

    Windows:
	    python -m venv venv
	    venv\Scripts\activate
    MacOS/Linux:
	    python3 -m venv venv
	    source venv/bin/activate


3. **Gereksinimleri yükleyin**:

Proje dizininde `requirements.txt` dosyasını kullanarak gerekli Python paketlerini yükleyin: 
	pip install -r requirements.txt


4. **NLTK veri setlerini indirin**:

Proje için gereken NLTK veri setlerini indirin. Python terminalinden aşağıdaki komutları çalıştırın:
```python
	import nltk
	nltk.download('stopwords')
	nltk.download('punkt')


5. **Uygulamayı çalıştırın**:
Proje dizininde aşağıdaki komutu çalıştırarak Flask uygulamasını başlatın:

	python app.py


6. **Uygulamayı tarayıcıda açın**:

	http://127.0.0.1:5000