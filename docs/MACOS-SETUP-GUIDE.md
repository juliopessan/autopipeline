# 🍎 Guia de Setup para macOS - Azure Autonomous Data Platform

## 🔍 Diagnóstico: Qual é o problema?

Execute estes comandos para ver o que está faltando:

```bash
# Verificar Python
python3 --version
which python3

# Verificar pip
pip3 --version
which pip3

# Verificar Node
node --version
npm --version

# Verificar Git
git --version
```

## ✅ Pré-requisitos para macOS

### 1. Instalar Python 3.11+ (se não tiver)

**Opção A: Usar Homebrew (Recomendado)**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python 3.11
brew install python@3.11

# Verificar
python3.11 --version
```

**Opção B: Download direto**
```bash
# Ir para https://www.python.org/downloads/
# Download Python 3.11 ou 3.12 para macOS
# Executar o instalador
```

### 2. Instalar Node.js 18+ (se não tiver)

```bash
# Com Homebrew
brew install node@18

# ou
brew install node

# Verificar
node --version
npm --version
```

### 3. Clonar o Repositório

```bash
git clone https://github.com/juliopessan/autopipeline.git
cd autopipeline
```

---

## 🚀 Opção 1: Rodando com Python Puro (Mais Fácil)

### Backend (Terminal 1)

```bash
cd ~/autopipeline

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r backend/backend_requirements.txt

# Definir chave API
export ANTHROPIC_API_KEY=sk-seu-chave-aqui

# Rodar backend
python backend/backend_main.py

# Deve aparecer:
# INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Frontend (Terminal 2)

```bash
cd ~/autopipeline/frontend

# Instalar dependências (primeira vez)
npm install

# Rodar frontend
npm start

# Deve aparecer:
# webpack compiled successfully
# Compiled successfully!
# You can now view autopipeline in the browser.
# Local: http://localhost:3000
```

### Acessar

- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🐳 Opção 2: Usando Docker Compose (Mais Fácil)

### Pré-requisitos

```bash
# Instalar Docker Desktop para macOS
# Ir para: https://www.docker.com/products/docker-desktop
# Download para macOS (Apple Silicon ou Intel)
# Instalar e abrir

# Verificar
docker --version
docker-compose --version
```

### Rodar com Docker Compose

```bash
cd ~/autopipeline

# Criar arquivo .env
cp .env.example .env

# Editar .env com sua API key
nano .env
# Mudar: ANTHROPIC_API_KEY=sk-sua-chave-aqui

# Rodar containers
docker-compose up -d

# Ver logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Acessar
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs

# Parar
docker-compose down
```

---

## ⚠️ Problemas Comuns no macOS

### Problema 1: "python: command not found"

**Solução:**
```bash
# Use python3 em vez de python
python3 --version

# Se usar python3, todos os comandos são:
python3 -m venv venv
source venv/bin/activate
pip3 install -r backend/backend_requirements.txt
python3 backend/backend_main.py
```

### Problema 2: "Permission denied" ao rodar venv

**Solução:**
```bash
# Remover venv antigo
rm -rf venv

# Criar novo
python3 -m venv venv
source venv/bin/activate
```

### Problema 3: "ModuleNotFoundError: No module named 'fastapi'"

**Solução:**
```bash
# Certifique-se que venv está ativado
source venv/bin/activate

# Reinstalar dependências
pip install --upgrade pip
pip install -r backend/backend_requirements.txt

# Verificar instalação
pip list | grep -i fastapi
```

### Problema 4: "Port 8000 already in use"

**Solução:**
```bash
# Encontrar e matar processo na porta 8000
lsof -ti:8000 | xargs kill -9

# Ou trocar porta no backend_main.py
# Mudar: uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Problema 5: "Port 3000 already in use"

**Solução:**
```bash
# Ir para frontend
cd frontend

# Rodar em porta diferente
PORT=3001 npm start
```

### Problema 6: "Command not found: npm"

**Solução:**
```bash
# Instalar Node.js
brew install node

# Verificar
node --version
npm --version
```

---

## 📋 Passo-a-Passo Completo (macOS)

### 1. Preparar Ambiente

```bash
# 1.1 Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 1.2 Instalar Python e Node
brew install python@3.11 node

# 1.3 Verificar
python3.11 --version
node --version
```

### 2. Clonar e Setup

```bash
# 2.1 Clonar
git clone https://github.com/juliopessan/autopipeline.git
cd autopipeline

# 2.2 Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# 2.3 Instalar dependências backend
pip install -r backend/backend_requirements.txt

# 2.4 Instalar dependências frontend
cd frontend
npm install
cd ..
```

### 3. Configurar Variáveis

```bash
# 3.1 Criar .env
cp .env.example .env

# 3.2 Editar (adicionar sua API key)
# nano .env
# ANTHROPIC_API_KEY=sk-sua-chave-aqui
```

### 4. Rodar Backend

```bash
# 4.1 Ativar venv (se não estiver)
source venv/bin/activate

# 4.2 Definir API key
export ANTHROPIC_API_KEY=sk-sua-chave-aqui

# 4.3 Rodar
python backend/backend_main.py

# Deve ver:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# Pressionar CTRL+C para parar
```

### 5. Rodar Frontend (Novo Terminal)

```bash
# 5.1 Ir para frontend
cd autopipeline/frontend

# 5.2 Rodar
npm start

# Deve abrir http://localhost:3000 automaticamente
```

### 6. Acessar

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs

---

## 🎯 Opção Recomendada para macOS

### **Opção 1: Python Puro (Mais Simples)**

Se tiver problemas com Docker, use Python puro:

```bash
# Terminal 1 - Backend
cd ~/autopipeline
source venv/bin/activate
export ANTHROPIC_API_KEY=sk-seu-chave
python backend/backend_main.py

# Terminal 2 - Frontend
cd ~/autopipeline/frontend
npm start
```

### **Opção 2: Docker Compose (Mais Robusto)**

Se quiser usar Docker:

```bash
cd ~/autopipeline
cp .env.example .env
# Editar .env com sua API key
docker-compose up
```

---

## ✅ Checklist de Setup

- [ ] Python 3.11+ instalado (`python3.11 --version`)
- [ ] Node.js 18+ instalado (`node --version`)
- [ ] Repositório clonado (`git clone ...`)
- [ ] Ambiente virtual criado (`python3.11 -m venv venv`)
- [ ] Venv ativado (`source venv/bin/activate`)
- [ ] Dependências instaladas (`pip install -r backend/backend_requirements.txt`)
- [ ] .env criado com ANTHROPIC_API_KEY
- [ ] Frontend dependências (`cd frontend && npm install`)
- [ ] Backend rodando (`python backend/backend_main.py` no Terminal 1)
- [ ] Frontend rodando (`npm start` no Terminal 2)
- [ ] Frontend acessível em http://localhost:3000
- [ ] Backend acessível em http://localhost:8000/docs

---

## 🚀 Próximas Ações

Depois de rodar com sucesso:

1. **Testar Dashboard:**
   - Criar programa
   - Rodar experimento
   - Ver métricas em tempo real

2. **Explorar Documentação:**
   - Ler docs/RUN-NOW.md
   - Estudar docs/FULLSTACK-SUMMARY.md
   - Revisar docs/azure_platform_architecture.md

3. **Deploy para Azure:**
   - Seguir docs/SETUP-DEPLOYMENT-GUIDE.md
   - Configurar Azure services
   - Deploy Docker container

---

## 📞 Precisa de Ajuda?

Se tiver problemas:

1. Verifique a saída do terminal (copy/paste do erro)
2. Confirme que todos os pré-requisitos estão instalados
3. Tente a Opção 1 (Python puro) primeiro
4. Se não funcionar, tente Docker Compose
5. Abra issue no GitHub se for bug específico

---

**Bom desenvolvimento! 🚀**

