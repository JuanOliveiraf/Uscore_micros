# 🔧 Guia de Instalação e Configuração do MongoDB no Windows

## ❌ Problema Atual
```
ServerSelectionTimeoutError: localhost:27017: [WinError 10061] 
Nenhuma conexão pôde ser feita porque a máquina de destino as recusou ativamente
```

**Causa**: O MongoDB não está instalado ou não está rodando na porta 27017.

## 📥 Solução: Instalar e Configurar o MongoDB

### Opção 1: Instalar MongoDB Community Edition (Recomendado)

#### 1️⃣ Download
- Acesse: https://www.mongodb.com/try/download/community
- Selecione a versão mais recente para Windows
- Baixe o instalador `.msi`

#### 2️⃣ Instalação
1. Execute o instalador `.msi`
2. Escolha "Complete" installation
3. **IMPORTANTE**: Marque a opção "Install MongoDB as a Service"
   - Isso fará o MongoDB iniciar automaticamente com o Windows
4. Marque "Install MongoDB Compass" (opcional, mas útil para visualizar dados)
5. Clique em "Install"

#### 3️⃣ Iniciar o Serviço
Abra o PowerShell como Administrador e execute:

```powershell
# Iniciar o serviço MongoDB
Start-Service MongoDB

# Verificar o status
Get-Service MongoDB

# Configurar para iniciar automaticamente
Set-Service -Name MongoDB -StartupType Automatic
```

#### 4️⃣ Testar a Conexão
```powershell
# Conectar ao MongoDB shell
mongosh

# No shell do MongoDB:
show dbs
exit
```

### Opção 2: Instalar via Chocolatey (Mais Rápido)

Se você tem o Chocolatey instalado:

```powershell
# Abrir PowerShell como Administrador
choco install mongodb -y

# Instalar MongoDB como serviço
mongod --install --serviceName "MongoDB" --serviceDisplayName "MongoDB" --dbpath "C:\data\db"

# Criar diretório de dados
New-Item -Path "C:\data\db" -ItemType Directory -Force

# Iniciar o serviço
Start-Service MongoDB
```

### Opção 3: MongoDB Portable (Sem Instalação)

#### 1️⃣ Download
- Baixe o arquivo ZIP do MongoDB Community: https://www.mongodb.com/try/download/community
- Escolha "ZIP Archive"

#### 2️⃣ Extrair e Configurar
```powershell
# Extrair para C:\mongodb (ou outro local de sua preferência)
Expand-Archive -Path "caminho\do\mongodb.zip" -DestinationPath "C:\mongodb"

# Criar pasta para dados
New-Item -Path "C:\mongodb\data" -ItemType Directory -Force

# Criar pasta para logs
New-Item -Path "C:\mongodb\logs" -ItemType Directory -Force
```

#### 3️⃣ Iniciar o MongoDB Manualmente
Abra um novo terminal PowerShell e execute:

```powershell
cd C:\mongodb\bin
.\mongod.exe --dbpath "C:\mongodb\data" --logpath "C:\mongodb\logs\mongo.log"
```

**Mantenha este terminal aberto** enquanto estiver usando a aplicação.

## ✅ Verificar se o MongoDB Está Rodando

### Método 1: Verificar o Serviço
```powershell
Get-Service MongoDB
```

**Status esperado**: `Running`

### Método 2: Verificar a Porta
```powershell
Test-NetConnection -ComputerName localhost -Port 27017
```

**Resultado esperado**: `TcpTestSucceeded : True`

### Método 3: Testar Conexão com mongosh
```powershell
mongosh mongodb://localhost:27017
```

## 🚀 Após Iniciar o MongoDB

1. **Reinicie o servidor FastAPI**
   ```powershell
   # Se já estiver rodando, pare com CTRL+C e inicie novamente
   python run.py
   ```

2. **Teste a API**
   ```powershell
   # Teste o health check
   curl http://localhost:8000/health
   
   # Teste criar um player
   curl -X POST "http://localhost:8000/api/players/" `
     -H "Content-Type: application/json" `
     -d '{\"name\":\"João Silva\",\"email\":\"joao@example.com\",\"age\":25,\"position\":\"Atacante\",\"team\":\"Team A\",\"active\":true}'
   ```

## 🎯 Comandos Úteis do MongoDB

```powershell
# Iniciar o serviço
Start-Service MongoDB

# Parar o serviço
Stop-Service MongoDB

# Reiniciar o serviço
Restart-Service MongoDB

# Verificar status
Get-Service MongoDB

# Ver logs (se instalado como serviço)
Get-Content "C:\Program Files\MongoDB\Server\7.0\log\mongod.log" -Tail 50
```

## 📊 Usando MongoDB Compass (Interface Gráfica)

Se você instalou o MongoDB Compass:

1. Abra o MongoDB Compass
2. Conecte-se usando a URI: `mongodb://localhost:27017`
3. Você verá o banco de dados `uscore_players` aparecer após criar o primeiro jogador
4. Explore as collections e documentos visualmente

## 🐳 Alternativa: MongoDB Atlas (Cloud - Grátis)

Se você não quiser instalar localmente:

1. Acesse: https://www.mongodb.com/cloud/atlas/register
2. Crie uma conta gratuita
3. Crie um cluster gratuito (M0)
4. Obtenha a connection string
5. Atualize o arquivo `.env`:
   ```
   MONGODB_URL=mongodb+srv://usuario:senha@cluster.mongodb.net/
   DATABASE_NAME=uscore_players
   PORT=8000
   ```

## ❗ Problemas Comuns

### Erro: "Access Denied"
**Solução**: Execute o PowerShell como Administrador

### Erro: "mongod não é reconhecido"
**Solução**: Adicione o MongoDB ao PATH do Windows
```powershell
$env:Path += ";C:\Program Files\MongoDB\Server\7.0\bin"
```

### Porta 27017 já em uso
**Solução**: Encontre e mate o processo
```powershell
# Ver o que está usando a porta
netstat -ano | findstr :27017

# Matar o processo (substitua PID pelo número retornado)
Stop-Process -Id PID -Force
```

### MongoDB não inicia
**Solução**: Verifique os logs
```powershell
Get-Content "C:\Program Files\MongoDB\Server\7.0\log\mongod.log" -Tail 100
```

## 📌 Resumo Rápido

```powershell
# 1. Instalar MongoDB (escolha um método acima)
# 2. Criar diretório de dados (se necessário)
New-Item -Path "C:\data\db" -ItemType Directory -Force

# 3. Iniciar MongoDB
Start-Service MongoDB
# OU
mongod --dbpath "C:\data\db"

# 4. Verificar
Test-NetConnection -ComputerName localhost -Port 27017

# 5. Iniciar a API
python run.py

# 6. Testar
curl http://localhost:8000/health
```

## 🎉 Pronto!

Após seguir estes passos, seu MongoDB estará rodando e a API funcionará perfeitamente!
