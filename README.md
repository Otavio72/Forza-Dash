# 🏎️📊 Forza Dash

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
![Página Inicial](assets/1.png)

![Página Inicial](assets/2.png)

### Login
![Página Inicial](assets/3.png)

### Página de Registro
![Página de Registro](assets/4.png)

### Página de Historico
![Página de Análise](assets/5.png)

### Página de Perfil
![Página de Análise](assets/6.png)

---

### dashboard em ação
![Datalogger](assets/gif1.gif)

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
[Forza Dash](https://fm7dashdemo.onrender.com)

# Autor
Otávio Ribeiro
[🔗LinkedIn](https://www.linkedin.com/in/otavio-ribeiro-57a359197)






