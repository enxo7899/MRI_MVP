# 🧪 Testing Guide - Albanian MOH Medical Imaging Platform

## Quick Start

```bash
# Make startup script executable
chmod +x start.sh

# Start the platform
./start.sh
```

## Manual Start

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

## Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| **Albanian Dashboard** | http://localhost/ | None |
| **OHIF Viewer** | http://localhost/viewer | None |
| **Orthanc PACS** | http://localhost:8042 | admin / moh_admin_2024 |
| **MONAI Label API** | http://localhost:8000/info/ | None |

## Testing Workflow

### 1. Verify Services Are Running

```bash
# Check all containers are up
docker-compose ps

# Should show:
# - moh-nginx-gateway (healthy)
# - moh-orthanc-pacs (healthy)
# - moh-ohif-viewer (healthy)
# - moh-monai-ai (healthy)
# - moh-web-portal (healthy)
```

### 2. Test Orthanc PACS

```bash
# Check Orthanc is responding
curl http://localhost:8042/system

# Should return JSON with system info
```

**Web Interface:**
1. Open http://localhost:8042
2. Login: `admin` / `moh_admin_2024`
3. You should see the Orthanc Explorer interface

### 3. Upload Test DICOM Images

**Option A: Via Orthanc Web UI**
1. Go to http://localhost:8042
2. Click "Upload" button
3. Select DICOM files (.dcm)
4. Click "Start the upload"

**Option B: Via Command Line (if you have DICOM files)**
```bash
# Upload a DICOM file
curl -X POST http://localhost:8042/instances \
  --data-binary @your-dicom-file.dcm
```

**Option C: Download Sample DICOM**
```bash
# Download sample CT scan
mkdir -p test-data
cd test-data

# Get sample DICOM from public dataset
wget https://www.rubomedical.com/dicom_files/chest.dcm

# Upload to Orthanc
curl -X POST http://localhost:8042/instances \
  --data-binary @chest.dcm

cd ..
```

### 4. Test Albanian Dashboard

1. Open http://localhost/
2. You should see:
   - Albanian Ministry header
   - "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
   - System status indicators
   - Recent studies table (if you uploaded DICOM)
   - Albanian labels throughout

3. Click "Hape Imazhin" (Open Image) button
   - Should open OHIF Viewer in new tab

### 5. Test OHIF Viewer

1. Open http://localhost/viewer
2. If you uploaded studies, they should appear in the study list
3. Click on a study to view images
4. Test viewer controls:
   - Zoom (mouse wheel)
   - Pan (right-click drag)
   - Window/Level (left-click drag)

### 6. Test MONAI Label API

```bash
# Check MONAI Label is running
curl http://localhost:8000/info/

# Should return JSON with app info including:
# - name_al: "Platforma AI e Imazherisë Mjekësore"
# - institution_al: "Ministria e Shëndetësisë..."
# - available_labels_al: (number of Albanian labels)
```

### 7. Test Nginx Routing

```bash
# Test dashboard
curl -I http://localhost/

# Test OHIF viewer
curl -I http://localhost/viewer

# Test Orthanc proxy
curl http://localhost/pacs/system

# Test MONAI proxy
curl http://localhost/monai/info/
```

## Troubleshooting

### Services Not Starting

```bash
# View logs for specific service
docker-compose logs orthanc
docker-compose logs monailabel
docker-compose logs web-portal

# Restart a service
docker-compose restart orthanc
```

### Orthanc Not Accessible

```bash
# Check if Orthanc is running
docker-compose ps orthanc

# Check logs
docker-compose logs orthanc

# Verify port is accessible
curl http://localhost:8042/system
```

### MONAI Label Slow to Start

MONAI Label takes 2-3 minutes to start initially. Check logs:

```bash
docker-compose logs -f monailabel

# Wait for:
# "MONAI Label - Sistemi AI i Imazherisë"
# "Datastore i inicializuar"
```

### Dashboard Not Loading

```bash
# Check web-portal logs
docker-compose logs web-portal

# Rebuild if needed
docker-compose up -d --build web-portal
```

### CORS Issues in Browser

Check browser console. If you see CORS errors:

```bash
# Restart nginx
docker-compose restart nginx

# Verify nginx config
docker-compose exec nginx nginx -t
```

## Verifying Albanian Localization

### Check Dashboard Labels

Open http://localhost/ and verify:
- ✅ "Ministria e Shëndetësisë dhe Mbrojtjes Sociale"
- ✅ "Studimet e Fundit" (Recent Studies)
- ✅ "Emri i Pacientit" (Patient Name)
- ✅ "Hape Imazhin" (Open Image)
- ✅ "AI Gati" (AI Ready)

### Check MONAI API Labels

```bash
curl http://localhost:8000/info/ | jq .

# Should include:
# - name_al
# - institution_al
# - available_labels_al
```

### Check Anatomy Labels

```bash
# View Albanian anatomy dictionary
docker-compose exec monailabel python3 -c "
from apps.ministry_app.lib.utils.albanian_labels import ANATOMY_EN_TO_AL
print('Sample Albanian labels:')
for eng, alb in list(ANATOMY_EN_TO_AL.items())[:10]:
    print(f'  {eng:20} -> {alb}')
"
```

## Performance Testing

### Upload Multiple Studies

```bash
# Upload 10 test studies
for i in {1..10}; do
  curl -X POST http://localhost:8042/instances \
    --data-binary @test-data/chest.dcm
  sleep 1
done
```

### Check Dashboard Response Time

```bash
# Time the dashboard load
time curl -s http://localhost/ > /dev/null

# Should be < 1 second
```

### Check PACS Query Performance

```bash
# Time study list retrieval
time curl -s http://localhost:8042/studies > /dev/null
```

## Clean Up

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## Next Steps

### Enable AI Models

To enable TotalSegmentator and MedSAM:

1. Edit `monai-app/apps/ministry_app/main.py`
2. Uncomment the AI model initialization code in `init_infers()`
3. Rebuild: `docker-compose up -d --build monailabel`
4. Models will download on first use (may take time)

### Add PostgreSQL

To enable PostgreSQL for better performance:

1. Uncomment PostgreSQL service in `docker-compose.yml`
2. Update `config/orthanc.json` with PostgreSQL config
3. Restart: `docker-compose up -d`

### Enable GPU

For GPU-accelerated AI inference:

1. Install nvidia-docker
2. Uncomment `runtime: nvidia` in `docker-compose.yml`
3. Restart: `docker-compose up -d monailabel`

## Support

For issues, check:
- Docker logs: `docker-compose logs`
- Service status: `docker-compose ps`
- System resources: `docker stats`

---

**Ministria e Shëndetësisë dhe Mbrojtjes Sociale**  
Republika e Shqipërisë
