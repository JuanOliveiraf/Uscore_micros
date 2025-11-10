# 🚀 Guia Rápido - Players Service

## ✅ Status: Servidor Rodando!

O servidor está rodando em: **http://localhost:8000**

## 🧪 Testando com Postman

### 1. Health Check ✅
```
GET http://localhost:8000/health
```
**Resposta esperada:**
```json
{
  "status": "healthy"
}
```

### 2. Criar um Jogador ✅
```
POST http://localhost:8000/api/players/
Content-Type: application/json

{
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "age": 25,
  "position": "Atacante",
  "team": "Team A",
  "active": true
}
```
**Resposta esperada (201):**
```json
{
  "id": "1",
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "age": 25,
  "position": "Atacante",
  "team": "Team A",
  "active": true,
  "created_at": "2025-10-20T12:00:00",
  "updated_at": "2025-10-20T12:00:00"
}
```

💡 **Dica**: Copie o `id` retornado para usar nos próximos testes!

### 3. Listar Todos os Jogadores ✅
```
GET http://localhost:8000/api/players/?skip=0&limit=10
```

### 4. Buscar Jogador por ID ✅
```
GET http://localhost:8000/api/players/1
```
(Substitua `1` pelo ID retornado na criação)

### 5. Buscar Jogadores ✅
```
GET http://localhost:8000/api/players/search?q=João
```

### 6. Atualizar Jogador ✅
```
PUT http://localhost:8000/api/players/1
Content-Type: application/json

{
  "name": "João Silva Atualizado",
  "position": "Meio-Campo",
  "age": 26
}
```

### 7. Deletar Jogador ✅
```
DELETE http://localhost:8000/api/players/1
```
**Resposta esperada:** 204 No Content

## 📊 Documentação Interativa

Acesse no navegador:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 💾 Onde estão os dados?

Os dados ficam salvos em:
```
./data/uscore_players.json
```

Você pode abrir este arquivo e ver todos os jogadores cadastrados!

## 🎯 Fluxo de Teste Completo

1. ✅ GET /health → Verificar que API está funcionando
2. ✅ POST /api/players/ → Criar jogador (anote o ID retornado)
3. ✅ GET /api/players/ → Ver lista de jogadores
4. ✅ GET /api/players/{id} → Buscar jogador específico
5. ✅ GET /api/players/search?q=João → Buscar por nome
6. ✅ PUT /api/players/{id} → Atualizar jogador
7. ✅ GET /api/players/{id} → Verificar atualização
8. ✅ DELETE /api/players/{id} → Deletar jogador
9. ✅ GET /api/players/{id} → Verificar deleção (deve retornar 404)

## 🐛 Troubleshooting

### Erro de Conexão?
- ✅ Verifique se o servidor está rodando
- ✅ Confirme a URL: `http://localhost:8000`
- ✅ Não precisa MongoDB instalado!

### Erro 422 (Validation Error)?
- ✅ Verifique o formato do email
- ✅ Certifique-se que campos obrigatórios estão presentes
- ✅ `name` e `email` são obrigatórios

### Erro 404 (Not Found)?
- ✅ Verifique se o ID do jogador existe
- ✅ Use um ID retornado pela API
- ✅ Confirme a URL do endpoint

## 📝 Exemplos Prontos

### Criar Goleiro
```json
{
  "name": "Carlos Oliveira",
  "email": "carlos@example.com",
  "age": 28,
  "position": "Goleiro",
  "team": "Team B",
  "active": true
}
```

### Criar Zagueiro
```json
{
  "name": "Pedro Santos",
  "email": "pedro@example.com",
  "age": 24,
  "position": "Zagueiro",
  "team": "Team A",
  "active": true
}
```

### Criar Meio-Campo
```json
{
  "name": "Lucas Ferreira",
  "email": "lucas@example.com",
  "age": 22,
  "position": "Meio-Campo",
  "team": "Team C",
  "active": true
}
```

## 🎉 Pronto!

Sua API está funcionando perfeitamente com TinyDB!

**Benefícios:**
- ✅ Sem necessidade de MongoDB
- ✅ Dados em arquivo JSON visível
- ✅ Fácil de fazer backup
- ✅ Perfeito para desenvolvimento

Se tiver dúvidas, consulte:
- `README.md` - Documentação completa
- `TESTING_GUIDE.md` - Guia detalhado de testes
- `TINYMONGO_INFO.md` - Informações sobre TinyDB vs MongoDB
