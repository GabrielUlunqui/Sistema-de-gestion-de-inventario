# Sistema de Gestión de Inventario

Aplicación full-stack con **FastAPI + SQLite** en el backend y **React (Vite)** en el frontend.

## Estructura

```
inventario/
├── backend/
│   ├── main.py              # Punto de entrada (uvicorn)
│   ├── requirements.txt
│   ├── inventario.db        # Base de datos SQLite (se crea sola)
│   └── app/
│       ├── __init__.py      # App factory + CORS
│       ├── database.py      # Engine SQLAlchemy + seed de datos
│       ├── models.py        # Modelo Item (ORM)
│       ├── schemas.py       # Esquemas Pydantic + validaciones
│       ├── crud.py          # Operaciones de base de datos
│       └── routers/
│           ├── items.py     # Endpoints /api/items
│           └── stats.py     # Endpoint /api/stats
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js       # Proxy /api -> :8000
│   └── src/
│       ├── main.jsx
│       ├── App.jsx          # Estado principal
│       ├── api.js           # Cliente Axios
│       ├── index.css        # Sistema de diseño oscuro
│       └── components/
│           ├── StatsBar.jsx        # Tarjetas de estadísticas
│           ├── Toolbar.jsx         # Búsqueda + filtros
│           ├── InventoryTable.jsx  # Tabla con stock inline
│           ├── ItemForm.jsx        # Modal agregar/editar
│           └── Toast.jsx           # Notificaciones
│
├── setup.bat                # Instala todo (venv + npm)
├── run.bat                  # Levanta backend + frontend
└── README.md
```

## Inicio rápido (Windows)

```bat
setup.bat     :: una sola vez: crea venv, instala dependencias
run.bat       :: levanta la app completa
```

| Servicio | URL |
|---|---|
| Frontend React | http://localhost:5173 |
| Backend FastAPI | http://127.0.0.1:8000 |
| Swagger UI | http://127.0.0.1:8000/docs |

## Funcionalidades

- **CRUD completo** de ítems: nombre, SKU, categoría, marca, precio, stock mínimo
- **Categorías**: Centrales, Teclados, GPRS, Sensores, Cámaras, DVR, Almacenamiento, Cables, Fuentes, Conectores
- **Marcas**: campo libre con sugerencias por categoría (Teclados: A2K4, A2K4 NG, DSC, Intelbras, Paradox · Sensores: DSC, Paradox, Hikvision)
- **Control de stock**: botones +/- inline, sin stock negativo (validado en cliente y servidor)
- **Alertas automáticas**: badge de "Stock bajo" cuando `cantidad <= stock mínimo`, "Sin stock" en 0
- **Dashboard**: total de productos, unidades, valor del inventario, alertas
- **Búsqueda y filtros**: por nombre/SKU/categoría/marca, por estado, categoría y marca
- **Seed automático**: la primera vez carga 15 productos de ejemplo

## API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/items/` | Listar (params: `search`, `status`, `category`, `brand`) |
| `POST` | `/api/items/` | Crear ítem |
| `GET` | `/api/items/{id}` | Obtener ítem |
| `PUT` | `/api/items/{id}` | Editar ítem |
| `PATCH` | `/api/items/{id}/stock` | Ajustar stock (`{"delta": ±n}`) |
| `DELETE` | `/api/items/{id}` | Eliminar ítem |
| `GET` | `/api/stats/` | Estadísticas del inventario |

## Ejecución manual

```bat
:: Backend
cd backend
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python main.py

:: Frontend (otra terminal)
cd frontend
npm install
npm run dev
```
