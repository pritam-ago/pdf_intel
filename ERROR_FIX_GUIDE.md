# PDF Intelligence System - Error Fix Guide

## Current Issues Found:

1. ✅ **Python Dependencies Fixed** - Updated to compatible versions
2. ❌ **Docker Desktop not running** - Qdrant needs Docker
3. ❌ **Services not started in correct order**

## Step-by-Step Fix:

### 1. Start Docker Desktop

- Open Docker Desktop application
- Wait for it to fully start (green icon in system tray)

### 2. Start Qdrant Vector Database

```bash
# Run this command:
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Start Python Service (in new terminal)

```bash
cd E:\sem3\APP\pdfis\service
venv\Scripts\activate.bat
python app.py
```

### 4. Start Java Backend (in new terminal)

```bash
cd E:\sem3\APP\pdfis\server
mvn spring-boot:run
```

### 5. Start Frontend (in new terminal)

```bash
cd E:\sem3\APP\pdfis\client
npm run dev
```

## Quick Test:

- Open http://localhost:3000 in browser
- Upload a PDF file
- Search for content

## Alternative: Use the batch files

1. Start Docker Desktop first
2. Run: `start-qdrant.bat`
3. Run: `start-python-service.bat`
4. Run: `start-java-backend.bat`
5. Run: `start-frontend.bat`

The system should work once all services are running!
