# 📚 Documentação do Projeto - Índice

## 🎯 Documentos Principais

### 1. [README.md](README.md) - Documentação Principal ⭐
- Visão geral do projeto
- Instalação e configuração
- Arquitetura com diagramas Mermaid
- Endpoints da API
- Estrutura do projeto

### 2. [QUICK_START.md](QUICK_START.md) - Guia Rápido 🚀
- Como começar em minutos
- Exemplos práticos de requisições
- Fluxo de teste completo
- Troubleshooting comum

### 3. [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guia de Testes 🧪
- Como usar as collections
- Casos de teste detalhados
- Checklist de validação
- Exemplos de respostas esperadas

### 4. [TINYMONGO_INFO.md](TINYMONGO_INFO.md) - Sobre TinyDB 💡
- Por que usamos TinyDB ao invés de MongoDB
- Comparação TinyDB vs MongoDB
- Como migrar para MongoDB em produção
- Vantagens e limitações

### 5. [MONGODB_SETUP.md](MONGODB_SETUP.md) - Setup MongoDB (Opcional) 🔧
- Como instalar MongoDB (se quiser usar)
- Configuração Windows
- Alternativas (Atlas, Chocolatey, etc)
- Solução de problemas

## 📁 Arquivos de Collection

### Postman
- [players_api.postman_collection.json](players_api.postman_collection.json)
  - Collection completa para Postman
  - Variáveis de ambiente configuradas
  - Scripts automáticos

### Insomnia
- [players_api.insomnia.json](players_api.insomnia.json)
  - Collection para Insomnia
  - Requisições organizadas
  - Ambiente pré-configurado

## 🗂️ Estrutura de Código

```
app/
├── main.py          → Aplicação FastAPI principal
├── config.py        → Configurações e variáveis de ambiente
├── database.py      → Conexão com TinyDB
├── models.py        → Modelos Pydantic (schemas)
├── repository.py    → Camada de acesso aos dados (CRUD)
└── routes.py        → Endpoints da API REST
```

## 🎯 Para Começar Agora

1. **Primeiro Acesso?** → Leia [QUICK_START.md](QUICK_START.md)
2. **Quer entender a arquitetura?** → Leia [README.md](README.md)
3. **Vai testar com Postman?** → Leia [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. **Quer usar MongoDB?** → Leia [MONGODB_SETUP.md](MONGODB_SETUP.md)
5. **Curiosidade sobre TinyDB?** → Leia [TINYMONGO_INFO.md](TINYMONGO_INFO.md)

## ⚡ Quick Commands

```bash
# Instalar dependências
pip install -r requirements.txt

# Rodar servidor
python run.py

# Acessar documentação interativa
http://localhost:8000/docs

# Ver dados salvos
cat ./data/uscore_players.json
```

## 📊 Endpoints Disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Informações da API |
| GET | `/health` | Health check |
| POST | `/api/players/` | Criar jogador |
| GET | `/api/players/` | Listar jogadores |
| GET | `/api/players/{id}` | Buscar por ID |
| GET | `/api/players/search?q=` | Buscar jogadores |
| PUT | `/api/players/{id}` | Atualizar jogador |
| DELETE | `/api/players/{id}` | Deletar jogador |

## 🎉 Features

- ✅ CRUD completo de jogadores
- ✅ Busca por nome, email, time, posição
- ✅ Paginação
- ✅ Validação de dados com Pydantic
- ✅ Documentação automática (Swagger/ReDoc)
- ✅ CORS habilitado
- ✅ Zero configuração (TinyDB)
- ✅ Collections prontas (Postman/Insomnia)
- ✅ Testes facilitados
- ✅ Dados em arquivo JSON visível

## 🤝 Contribuindo

1. Clone o repositório
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Faça suas alterações
4. Commit: `git commit -m 'Adiciona nova feature'`
5. Push: `git push origin feature/nova-feature`
6. Abra um Pull Request

## 📞 Suporte

- Dúvidas sobre instalação → [README.md](README.md)
- Problemas com testes → [TESTING_GUIDE.md](TESTING_GUIDE.md)
- Erro de conexão → [QUICK_START.md](QUICK_START.md#-troubleshooting)
- MongoDB não funciona → [MONGODB_SETUP.md](MONGODB_SETUP.md)

---

**Desenvolvido com** ❤️ **usando FastAPI e TinyDB**
