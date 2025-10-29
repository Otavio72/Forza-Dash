# 🏎️📊 FM7Dash

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Otavio72/Forza-Dash/blob/main/LICENSE)

---

## 🛠️ Sobre o projeto

**FM7Dash** é um dashboard web desenvolvido para receber dados em tempo real do jogo **Forza Motorsport 7** via **Socket UDP**, processá-los com **FastAPI** e exibi-los em uma interface interativa de gauges e gráficos.

O objetivo do projeto é demonstrar integração entre jogo e backend, processamento de telemetria e visualização dinâmica de dados — servindo como **projeto de portfólio técnico**.

---

### ⚡ Funcionalidades principais

- 📡 Recepção de dados em tempo real via **Socket UDP**
- 🔄 Comunicação com o frontend via **WebSocket**
- 📈 Dashboard dinâmico com **gráficos e gauges**
- 💾 Armazenamento dos dados em **SQLite**
- 🔐 Sistema básico de **login, registro e histórico**
- 🧠 Estrutura backend modular com **FastAPI**
- 🐳 Deploy containerizado com **Docker**

---

## 💻 Layout da aplicação

### Página inicial
![Página Inicial](assets/acs1.png)

### Página de Status
![Página de Status](assets/acs2.png)

### Menu de Sessões
![Menu de Sessões](assets/acs3.png)

### Página de Análise
![Página de Análise](assets/acs4.png)

---

## 🎞️ Demonstração

### Datalogger em ação
![Datalogger](assets/gif3.gif)

### Dentro do jogo
🎥 [Assista à demonstração no YouTube](https://www.youtube.com/watch?v=mdHSS1vnZvM)

---

## 🚀 Tecnologias utilizadas

### 🔙 Backend
- Python 3.11
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic

### 💾 Banco de dados
- SQLite

### 🎨 Frontend
- HTML
- CSS
- JavaScript

### 🐳 Containerização
- Docker

---

## ⚙️ Como executar o projeto

### ✅ Pré-requisitos
- **Python 3.11+** (para rodar localmente)
- **Docker** (para rodar a versão containerizada)

---

### 💻 Executando localmente

```bash
# Clonar o repositório
git clone https://github.com/Otavio72/FM7Dash.git
cd FM7Dash

# Criar e ativar ambiente virtual
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # (Windows)
# ou
source .venv/bin/activate      # (Linux/macOS)

# Instalar dependências
pip install -r requirements.txt

# Rodar a aplicação
uvicorn app.main:app --reload
```

🐳 Executando com Docker

```bash
# Construir a imagem

docker build -t fm7dash .

# Rodar o container
docker run -d -p 8000:8000 fm7dash
```

## 💻 Online
[PlayerHands](https://playerhandsdemo.onrender.com)

# Autor
Otávio Ribeiro
[🔗LinkedIn](https://www.linkedin.com/in/otavio-ribeiro-57a359197)


