# 📋 Guia de Teste - Players Service API

## ✅ Validação das Collections

### Collection do Postman
**Arquivo**: `players_api.postman_collection.json`

#### ✅ Estrutura Correta:
- ✅ Formato: Postman Collection v2.1.0
- ✅ Variáveis de ambiente: `baseUrl` e `player_id`
- ✅ Script automático para capturar `player_id` após criar um jogador
- ✅ Todas as requisições CRUD completas

#### 📂 Grupos de Requisições:

**1. Health Check**
- `GET /` - Root endpoint
- `GET /health` - Status do serviço

**2. Players (CRUD Completo)**
- `POST /api/players/` - Criar jogador (com script para salvar ID)
- `GET /api/players/` - Listar todos (paginação configurada)
- `GET /api/players/{player_id}` - Buscar por ID
- `GET /api/players/search?q=João` - Buscar por termo
- `PUT /api/players/{player_id}` - Atualizar jogador
- `DELETE /api/players/{player_id}` - Deletar jogador

**3. Exemplos Adicionais**
- Criar Goleiro
- Criar Zagueiro
- Criar Jogador Inativo
- Desativar Jogador
- Buscar por Time
- Buscar por Posição

### Collection do Insomnia
**Arquivo**: `players_api.insomnia.json`

#### ✅ Estrutura Correta:
- ✅ Formato: Insomnia v4
- ✅ Workspace configurado
- ✅ Ambiente base com variáveis
- ✅ Requisições organizadas em grupos

#### 📂 Grupos:
- Health Check (2 requisições)
- Players (6 requisições CRUD)

## 🧪 Como Testar

### Opção 1: Usando Postman

1. **Importar a Collection**
   ```
   Postman → Import → Selecione "players_api.postman_collection.json"
   ```

2. **Ordem de Testes Recomendada:**
   
   a. **Health Check**
   - Execute "Root" → Deve retornar informações da API
   - Execute "Health Check" → Deve retornar `{"status": "healthy"}`
   
   b. **Criar um Player**
   - Execute "Create Player" → Salva automaticamente o ID na variável `player_id`
   - Resposta esperada: `201 Created`
   
   c. **Listar Players**
   - Execute "Get All Players" → Lista todos os jogadores
   - Resposta esperada: `200 OK` com array de jogadores
   
   d. **Buscar Player Específico**
   - Execute "Get Player by ID" → Usa o `player_id` salvo automaticamente
   - Resposta esperada: `200 OK` com dados do jogador
   
   e. **Buscar Players**
   - Execute "Search Players" → Busca por "João"
   - Resposta esperada: `200 OK` com resultados filtrados
   
   f. **Atualizar Player**
   - Execute "Update Player" → Atualiza o jogador criado
   - Resposta esperada: `200 OK` com dados atualizados
   
   g. **Deletar Player**
   - Execute "Delete Player" → Remove o jogador
   - Resposta esperada: `204 No Content`

3. **Testar Exemplos Adicionais**
   - Crie jogadores de diferentes posições
   - Teste buscas por time e posição
   - Teste desativar jogadores

### Opção 2: Usando Insomnia

1. **Importar a Collection**
   ```
   Insomnia → Import/Export → Import Data → From File
   Selecione "players_api.insomnia.json"
   ```

2. **Configurar Variáveis**
   - A variável `baseUrl` já está definida como `http://localhost:8000`
   - Após criar um player, copie o `id` da resposta e cole na variável `player_id`

3. **Executar Requisições**
   - Siga a mesma ordem do Postman acima

### Opção 3: Usando cURL (Terminal)

```bash
# 1. Health Check
curl http://localhost:8000/

# 2. Criar Player
curl -X POST "http://localhost:8000/api/players/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "age": 25,
    "position": "Atacante",
    "team": "Team A",
    "active": true
  }'

# 3. Listar Players
curl "http://localhost:8000/api/players/?skip=0&limit=10"

# 4. Buscar Player por ID (substitua {id} pelo ID retornado)
curl "http://localhost:8000/api/players/{id}"

# 5. Buscar Players
curl "http://localhost:8000/api/players/search?q=João"

# 6. Atualizar Player (substitua {id})
curl -X PUT "http://localhost:8000/api/players/{id}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva Atualizado",
    "position": "Meio-Campo",
    "age": 26
  }'

# 7. Deletar Player (substitua {id})
curl -X DELETE "http://localhost:8000/api/players/{id}"
```

### Opção 4: Usando a Interface Swagger

1. Acesse: http://localhost:8000/docs
2. Interface interativa com todos os endpoints
3. Clique em "Try it out" para testar cada endpoint
4. Documentação automática e exemplos incluídos

## 🎯 Casos de Teste

### Teste 1: Fluxo Completo CRUD
```
1. POST /api/players/ → Criar jogador
2. GET /api/players/{id} → Verificar criação
3. PUT /api/players/{id} → Atualizar dados
4. GET /api/players/{id} → Verificar atualização
5. DELETE /api/players/{id} → Deletar
6. GET /api/players/{id} → Verificar deleção (404)
```

### Teste 2: Validação de Dados
```
1. POST com email inválido → Deve retornar erro 422
2. POST sem campos obrigatórios → Deve retornar erro 422
3. PUT com idade negativa → Deve retornar erro 422
```

### Teste 3: Busca e Filtros
```
1. Criar 3+ jogadores de times diferentes
2. Buscar por nome → Verificar resultados
3. Buscar por time → Verificar filtro
4. Buscar por posição → Verificar filtro
```

### Teste 4: Paginação
```
1. Criar 15 jogadores
2. GET /api/players/?skip=0&limit=5 → Primeiros 5
3. GET /api/players/?skip=5&limit=5 → Próximos 5
4. GET /api/players/?skip=10&limit=5 → Últimos 5
```

## ✅ Checklist de Validação

- [ ] Collection importa sem erros
- [ ] Todas as variáveis estão configuradas
- [ ] Health check retorna status 200
- [ ] Criar player retorna 201
- [ ] Player ID é capturado automaticamente (Postman)
- [ ] Listar players retorna array
- [ ] Buscar por ID retorna player correto
- [ ] Search funciona com diferentes termos
- [ ] Update retorna dados atualizados
- [ ] Delete retorna 204
- [ ] Buscar player deletado retorna 404

## 🔧 Solução de Problemas

### Erro de Conexão
```
Problema: "Connection refused"
Solução: Verificar se o servidor está rodando em http://localhost:8000
```

### Erro 404
```
Problema: "Not Found"
Solução: Verificar se a URL está correta (incluir /api/players/)
```

### Erro 422
```
Problema: "Validation Error"
Solução: Verificar se todos os campos obrigatórios estão preenchidos
         e se o email está no formato correto
```

### MongoDB Connection Error
```
Problema: "Could not connect to MongoDB"
Solução: Verificar se o MongoDB está rodando em mongodb://localhost:27017
```

## 📊 Respostas Esperadas

### POST /api/players/ (201 Created)
```json
{
  "id": "671234567890abcdef123456",
  "name": "João Silva",
  "email": "joao.silva@example.com",
  "age": 25,
  "position": "Atacante",
  "team": "Team A",
  "active": true,
  "created_at": "2025-10-20T12:00:00.000Z",
  "updated_at": "2025-10-20T12:00:00.000Z"
}
```

### GET /api/players/ (200 OK)
```json
[
  {
    "id": "671234567890abcdef123456",
    "name": "João Silva",
    "email": "joao.silva@example.com",
    "age": 25,
    "position": "Atacante",
    "team": "Team A",
    "active": true,
    "created_at": "2025-10-20T12:00:00.000Z",
    "updated_at": "2025-10-20T12:00:00.000Z"
  }
]
```

### GET /health (200 OK)
```json
{
  "status": "healthy"
}
```

## 🎉 Conclusão

As collections estão **100% corretas** e prontas para uso! Todos os endpoints estão mapeados corretamente e seguem as melhores práticas de APIs REST.
