# 🏥 Platforma Kombëtare AI e Imazherisë Mjekësore

## Ministria e Shëndetësisë dhe Mbrojtjes Sociale - Republika e Shqipërisë

National Medical Imaging AI Platform for the Albanian Ministry of Health

---

## 🇦🇱 Përmbledhje (Overview)

Kjo platformë ofron:
- **PACS Server** - Orthanc me PostgreSQL për ruajtjen e imazheve DICOM
- **AI Engine** - MONAI Label me TotalSegmentator dhe MedSAM
- **Medical Viewer** - OHIF Viewer për vizualizimin e imazheve
- **Web Dashboard** - Paneli Albanian i Ministrisë

This platform provides:
- **PACS Server** - Orthanc with PostgreSQL for DICOM image storage
- **AI Engine** - MONAI Label with TotalSegmentator and MedSAM
- **Medical Viewer** - OHIF Viewer for image visualization
- **Web Dashboard** - Albanian Ministry Dashboard

---

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (Mac/Windows) or Docker Engine (Linux)
- **Docker Compose** v1.27+
- **8GB+ RAM** recommended
- **20GB+ storage** for images and containers
- **Optional**: NVIDIA GPU with nvidia-docker for AI acceleration

### Deployment

**Option 1: Using Startup Script (Recommended)**

```bash
# Navigate to project
cd albania-moh-ai

# Make script executable (first time only)
chmod +x start.sh

# Start the platform
./start.sh
```

**Option 2: Manual Start**

```bash
# Build and start all services
docker-compose up -d --build

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**First startup takes 5-10 minutes** to build images and download dependencies.

### Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Dashboard** | http://localhost/ | None |
| **OHIF Viewer** | http://localhost/viewer | None |
| **Orthanc PACS** | http://localhost:8042 | admin / moh_admin_2024 |
| **MONAI Label** | http://localhost:8000/info/ | None |

### Testing

See **[TESTING.md](TESTING.md)** for comprehensive testing guide including:
- Service verification
- DICOM upload instructions
- Sample data download
- Albanian localization checks
- Troubleshooting steps

---

## 📁 Project Structure

```
albania-moh-ai/
├── docker-compose.yml          # Main orchestration
├── config/
│   ├── nginx.conf              # Reverse proxy configuration
│   ├── orthanc.json            # PACS server configuration
│   └── ohif-config.js          # OHIF viewer configuration
├── web-portal/                 # Next.js Albanian Dashboard
│   ├── app/
│   │   ├── page.tsx            # Main dashboard page
│   │   ├── layout.tsx          # App layout
│   │   └── globals.css         # Tailwind styles
│   ├── Dockerfile
│   └── package.json
└── monai-app/                  # AI Engine
    ├── apps/
    │   └── ministry_app/
    │       ├── main.py         # MONAI Label application
    │       └── lib/
    │           ├── configs/
    │           ├── inferers/
    │           │   ├── totalsegmentator.py
    │           │   └── medsam.py
    │           └── utils/
    │               ├── albanian_labels.py  # 🇦🇱 Albanian anatomy dict
    │               └── dicom_utils.py
    ├── requirements.txt
    └── Dockerfile
```

---

## 🏷️ Albanian Localization

All user-facing interfaces are in professional medical Albanian:

### Anatomical Labels (Etiketat Anatomike)

| English | Shqip |
|---------|-------|
| Liver | Mëlçia |
| Spleen | Shpretka |
| Left Lung | Mushkëria e Majtë |
| Right Lung | Mushkëria e Djathtë |
| Left Kidney | Veshka e Majtë |
| Right Kidney | Veshka e Djathtë |
| Heart | Zemra |
| Aorta | Aorta |
| Brain | Truri |
| Pancreas | Pankreasi |
| Stomach | Stomaku |
| Gallbladder | Fshikëza e Tëmthit |

Full mapping includes 100+ anatomical structures in `albanian_labels.py`.

### UI Labels

- **Hape Imazhin** - Open Image
- **AI Gati** - AI Ready
- **Studimet e Fundit** - Recent Studies
- **Emri i Pacientit** - Patient Name
- **Shiko** - View
- **Analizo** - Analyze

---

## 🔧 Configuration

### Environment Variables

```bash
# Orthanc
ORTHANC__AUTHENTICATION_ENABLED=false
ORTHANC__DICOM_AET=MOH_ALBANIA

# MONAI Label
MONAI_LABEL_APP=/app/apps/ministry_app
MONAI_LABEL_STUDIES=http://orthanc:8042/dicom-web

# Web Portal
NEXT_PUBLIC_PACS_URL=/pacs
NEXT_PUBLIC_VIEWER_URL=/viewer
NEXT_PUBLIC_MONAI_URL=/monai
```

### DICOM Import

Upload DICOM files via:

1. **Orthanc Explorer**: Navigate to http://localhost/pacs → Upload
2. **DICOMweb**: POST to `/pacs/dicom-web/studies`
3. **DICOM Protocol**: Send to `localhost:4242` (AET: MOH_ALBANIA)

---

## 🤖 AI Models

### TotalSegmentator

Automatic multi-organ segmentation (104+ structures):
- Organs: Liver, Spleen, Kidneys, etc.
- Cardiovascular: Heart, Aorta, Vessels
- Skeletal: Vertebrae, Ribs, Bones
- Muscles and Tissues

```bash
# API Endpoint
POST /monai/infer/totalsegmentator
```

### MedSAM (Interactive)

Bounding box-based interactive segmentation:
- User draws bounding box
- Model generates precise segmentation
- Output labeled as "Zonë e Përzgjedhur"

```bash
# API Endpoint
POST /monai/infer/medsam
{
  "image": "<study_id>",
  "box": [x1, y1, x2, y2]
}
```

---

## 📊 DICOM SEG Output

All AI segmentations are saved as DICOM SEG with Albanian metadata:

```
SeriesDescription: "Analiza AI (Ministria)"
Manufacturer: "Republika e Shqipërisë"
InstitutionName: "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
SegmentLabel: <Albanian anatomical name>
```

---

## 🔒 Security Notes

This is an MVP deployment. For production:

1. Enable Orthanc authentication
2. Add HTTPS/TLS termination
3. Implement user authentication (e.g., OAuth2)
4. Configure firewall rules
5. Enable audit logging
6. Implement RBAC for different user roles

---

## 🐛 Troubleshooting

### Services not starting

```bash
# Check individual service logs
docker-compose logs orthanc
docker-compose logs monailabel
docker-compose logs web-portal

# Restart specific service
docker-compose restart <service_name>
```

### GPU not detected

```bash
# Verify NVIDIA runtime
docker run --rm --gpus all nvidia/cuda:11.8-base nvidia-smi

# Check MONAI Label logs
docker-compose logs monailabel | grep -i gpu
```

### CORS issues

Ensure nginx is properly configured with:
- `Cross-Origin-Opener-Policy: same-origin`
- `Cross-Origin-Embedder-Policy: require-corp`

---

## 📝 License

Government of Albania - Internal Use Only

---

## 📞 Support

**Ministria e Shëndetësisë dhe Mbrojtjes Sociale**  
Departamenti i Teknologjisë së Informacionit  
Bulevardi "Dëshmorët e Kombit", Tiranë, Shqipëri

---

*Built with MONAI, OHIF, Orthanc, and Next.js*
