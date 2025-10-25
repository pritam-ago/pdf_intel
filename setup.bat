@echo off
echo Setting up PDF Intelligence System...

echo Installing frontend dependencies...
cd client
npm install
cd ..

echo Installing Python dependencies...
cd service
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo Setup complete! 
echo.
echo To start the system:
echo 1. Run start-qdrant.bat (make sure Docker is running)
echo 2. Run start-python-service.bat
echo 3. Run start-java-backend.bat  
echo 4. Run start-frontend.bat
echo.
echo Then open http://localhost:3000 in your browser
pause
