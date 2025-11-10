# teamsService (FastAPI + TinyDB)

API de **Times** para o UScore — leve e local, usando TinyDB (JSON).

## 🚀 Como rodar
```bash
pip install -r requirements.txt
python run.py
```
Swagger: http://localhost:8001/docs

## 🔗 Endpoints
- `POST /api/v1/teams`
- `GET /api/v1/teams` (filtros: `university`, `sport`, `competitionId`, `q`)
- `GET /api/v1/teams/{id}`
- `PUT /api/v1/teams/{id}`
- `DELETE /api/v1/teams/{id}`
