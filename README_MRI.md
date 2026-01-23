# 🧠 Analiza e Skanimit MRI - Ministria e Shëndetësisë

## Republika e Shqipërisë 🇦🇱

Sistem AI për analizën e skanimeve MRI dhe zbulimin automatik të organeve.

---

## 🎯 Karakteristikat

- **Upload i Thjeshtë**: Ngarko skanime MRI direkt nga shfletuesi
- **Analiza Automatike**: AI zbulonorgan automatikisht
- **Raport në Shqip**: Rezultate të plota në gjuhën shqipe
- **Vizualizim**: Shfaqje e organeve të zbuluara me konfidencë
- **Ndërfaqe Profesionale**: Dizajn i përshtatur për mjekë

---

## 🚀 Quick Start

### Hapi 1: Start the Application

```bash
cd /Users/enxom/Desktop/MRI_MVP/albania-moh-ai

# Start the MRI analyzer
./start-mri.sh
```

### Hapi 2: Open in Browser

```
http://localhost:5000
```

### Hapi 3: Upload & Analyze

1. **Ngarko Skanimin**: Drag & drop ose kliko për të zgjedhur
2. **Formate të Pranuara**: `.nii`, `.nii.gz`, `.dcm`, `.png`, `.jpg`
3. **Kliko "Analizoni Skanimin"**
4. **Shiko Raportin**: Rezultate në shqip me organe të zbuluara

---

## 📋 Workflow (Si X-ray MVP)

```
1. User uploads MRI scan
   ↓
2. AI processes and segments organs
   ↓
3. System generates Albanian report
   ↓
4. User sees:
   - Detected organs with confidence %
   - Volume measurements
   - Status (Normal/Abnormal)
   - Recommendations in Albanian
```

---

## 🏥 Organet e Zbulueshme

### Organe Kryesore
- 🫀 Zemra (Heart)
- 🫁 Mushkëritë (Lungs)
- 🧠 Truri (Brain)
- 🫘 Mëlçia (Liver)
- 🫘 Shpretka (Spleen)
- 🫘 Veshkat (Kidneys)
- 🫘 Pankreasi (Pancreas)
- 🫘 Stomaku (Stomach)
- 🫘 Fshikëza e Tëmthit (Gallbladder)

### Sisteme të Tjera
- Sistemi Kardiovaskular
- Sistemi Tretës
- Sistemi Urinar
- Gjëndrat

---

## 📊 Rezultatet

### Për Çdo Organ:
- **Emri në Shqip**: Etiketë e plotë në gjuhën shqipe
- **Konfidenca**: Përqindja e saktësisë së zbulimit
- **Vëllimi**: Matje në mililitër (ml)
- **Statusi**: Normal / Anormal / I Zmadhuar / I Zvogëluar

### Raporti Përfshin:
- ✅ Përmbledhje e përgjithshme
- ✅ Lista e organeve të zbuluara
- ✅ Vizualizim me ngjyra
- ✅ Rekomandime mjekësore
- ✅ Paralajmërim për rishikim nga radiolog

---

## 🛠️ Technical Stack

- **Backend**: Flask (Python)
- **AI Engine**: Simulated segmentation (ready for TotalSegmentator integration)
- **Frontend**: Pure HTML/CSS/JavaScript
- **Localization**: Albanian translations
- **Deployment**: Docker

---

## 📁 Project Structure

```
mri-app/
├── app.py                  # Flask web server
├── engine_mri.py           # AI segmentation engine
├── translations.py         # Albanian labels & report generation
├── templates/
│   └── index.html          # Web interface
├── requirements.txt        # Python dependencies
└── Dockerfile              # Container configuration
```

---

## 🔧 Development

### Run Locally (without Docker)

```bash
cd mri-app

# Install dependencies
pip install -r requirements.txt

# Run app
python app.py

# Open browser
open http://localhost:5000
```

### Add Real AI Model

To integrate TotalSegmentator:

1. Edit `engine_mri.py`
2. Replace `simulate_organ_detection()` with actual TotalSegmentator call
3. Update `requirements.txt` to include `totalsegmentator`
4. Rebuild: `docker-compose -f docker-compose-simple.yml up -d --build`

---

## 📝 API Endpoints

### POST /analyze
Upload and analyze MRI scan

**Request:**
```
Content-Type: multipart/form-data
file: <MRI scan file>
```

**Response:**
```json
{
  "success": true,
  "organs_detected": 8,
  "total_organs": 50,
  "processing_time": 2.5,
  "report": {
    "summary": "Analiza identifikoi 8 organe...",
    "findings": [...],
    "recommendations": [...]
  }
}
```

### GET /health
Health check endpoint

---

## ⚠️ Paralajmërim i Rëndësishëm

Ky është një sistem prototipi për qëllime kërkimore dhe edukative.

- ❌ Rezultatet janë sugjerime, jo diagnoza përfundimtare
- ❌ Çdo rast duhet vlerësuar nga një radiolog i kualifikuar
- ❌ NUK duhet përdorur për vendime klinike pa mbikëqyrje mjekësore

---

## 🎨 Design Philosophy

Inspired by your X-ray MVP:
- **Clean & Minimal**: Focus on functionality
- **Albanian First**: All text in professional medical Albanian
- **Government Style**: Red/Black Albanian flag colors
- **User-Friendly**: Drag & drop, instant results
- **Professional**: Suitable for medical environment

---

## 🚀 Deployment

### Local Testing
```bash
./start-mri.sh
```

### Production Deployment
```bash
docker-compose -f docker-compose-simple.yml up -d --build
```

### Stop Service
```bash
docker-compose -f docker-compose-simple.yml down
```

---

## 📞 Support

**Ministria e Shëndetësisë dhe Mbrojtjes Sociale**  
Departamenti i Teknologjisë së Informacionit  
Bulevardi "Dëshmorët e Kombit", Tiranë, Shqipëri

---

## 🆚 Comparison with X-ray MVP

| Feature | X-ray MVP | MRI MVP |
|---------|-----------|---------|
| **Upload** | ✅ Drag & drop | ✅ Drag & drop |
| **AI Analysis** | ✅ 18 pathologies | ✅ 50+ organs |
| **Albanian UI** | ✅ Full | ✅ Full |
| **Report** | ✅ Probabilities | ✅ Organs + volumes |
| **Visualization** | ✅ Heatmap | ✅ Segmentation overlay |
| **Processing Time** | ✅ 2-3 sec | ✅ 2-5 sec |
| **Tech Stack** | Flask + DenseNet | Flask + Segmentation |

---

**Built with ❤️ for Ministria e Shëndetësisë - Republika e Shqipërisë 🇦🇱**
