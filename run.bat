@echo off
echo Iniciando backend (http://127.0.0.1:8000) y frontend (http://localhost:5173)...

start "Inventario - Backend" cmd /k "cd backend && call .venv\Scripts\activate.bat && python main.py"
start "Inventario - Frontend" cmd /k "cd frontend && npm run dev"

timeout /t 5 >nul
start http://localhost:5173
