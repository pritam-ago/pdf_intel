# PDF Intelligence System

A full-stack PDF intelligence system that allows users to upload PDF files and search through them using semantic search powered by vector embeddings.

## Architecture

- **Frontend**: Next.js with React (TypeScript)
- **Backend API**: Java Spring Boot
- **PDF Processing**: Python FastAPI service with PyPDF2 and Sentence Transformers
- **Vector Database**: Qdrant for semantic search

## Prerequisites

- Node.js and npm
- Java 8+ and Maven
- Python 3.8+
- Docker (for Qdrant)

## Quick Start

### 1. Start Qdrant Vector Database

```bash
# Make sure Docker is running, then:
./start-qdrant.bat
# Or manually:
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 2. Install Python Dependencies

```bash
cd service
python -m venv venv
venv\Scripts\activate.bat  # On Windows
pip install -r requirements.txt
```

### 3. Start Python Service

```bash
./start-python-service.bat
# Or manually:
cd service
python app.py
```

### 4. Start Java Backend

```bash
./start-java-backend.bat
# Or manually:
cd server
mvn spring-boot:run
```

### 5. Start Frontend

```bash
./start-frontend.bat
# Or manually:
cd client
npm install
npm run dev
```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Upload PDF files using drag-and-drop or file browser
3. Wait for files to be processed (they'll be chunked and embedded)
4. Search through your PDFs using natural language queries
5. View search results with relevance scores

## API Endpoints

### Java Backend (Port 8080)

- `GET /api/docs/health` - Health check
- `POST /api/docs/upload` - Upload PDF files
- `GET /api/docs/search?q=query` - Search through PDFs

### Python Service (Port 8000)

- `GET /` - Service health check
- `POST /upload` - Process PDF files
- `GET /search?q=query&k=5` - Semantic search

## Features

- **Multi-file Upload**: Upload multiple PDF files at once
- **Drag & Drop**: Intuitive file upload interface
- **Semantic Search**: Find relevant content using natural language
- **Real-time Processing**: Files are processed and indexed immediately
- **Error Handling**: Comprehensive error handling across all services
- **Responsive UI**: Modern, mobile-friendly interface

## File Structure

```
pdfis/
├── client/                 # Next.js frontend
│   ├── app/
│   │   ├── page.tsx       # Main upload/search interface
│   │   └── layout.tsx     # App layout
│   └── package.json
├── server/                 # Java Spring Boot backend
│   ├── src/main/java/com/example/pdfintel/
│   │   ├── controller/
│   │   │   └── DocController.java
│   │   └── PdfIntelApplication.java
│   └── pom.xml
├── service/               # Python FastAPI service
│   ├── app.py            # FastAPI application
│   ├── ingest.py         # PDF processing and vector operations
│   ├── requirements.txt  # Python dependencies
│   └── data/uploads/     # Uploaded PDF files
└── start-*.bat           # Startup scripts
```

## Troubleshooting

### Common Issues

1. **Qdrant Connection Error**: Make sure Docker is running and Qdrant is accessible at `localhost:6333`
2. **Python Dependencies**: Ensure all packages are installed in the virtual environment
3. **Port Conflicts**: Make sure ports 3000, 8000, and 8080 are available
4. **File Upload Errors**: Check that the `data/uploads` directory exists and is writable

### Service URLs

- Frontend: http://localhost:3000
- Java Backend: http://localhost:8080
- Python Service: http://localhost:8000
- Qdrant: http://localhost:6333

## Development

To modify the system:

1. **Frontend**: Edit files in `client/app/`
2. **Backend**: Modify Java controllers in `server/src/main/java/`
3. **PDF Processing**: Update Python code in `service/`

The system uses semantic search with sentence transformers, so search results are ranked by semantic similarity rather than keyword matching.
