# profileService (FastAPI + TinyDB)

Serviço de **Perfis de Usuários** com FastAPI + TinyDB, compatível com playersService e competitionsService.

## 🚀 Funcionalidades
- CRUD completo de perfis (user_id, display_name, bio, avatar_url)
- Favoritos de times e competições
- Busca e paginação
- Persistência local em `data/profiles.json`

## 🧱 Estrutura
```
app/
├── main.py
├── config.py
├── database.py
├── models.py
├── repository.py
├── routes.py
data/
└── profiles.json
```

## 🧩 Como rodar
```bash
pip install -r requirements.txt
python run.py
```

API: http://localhost:8000/docs
```

## 🔑 Observação
`user_id` é único e vem de outro serviço de autenticação.
