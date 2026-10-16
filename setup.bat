@echo off
echo === Instalando backend ===
cd backend
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo === Instalando frontend ===
cd frontend
npm install
cd ..

echo.
echo === Listo! Ejecuta run.bat para iniciar la app ===
pause
