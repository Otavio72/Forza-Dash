# Importa o router de autenticação
from app.routers.rota_auth import rota_auth

# Importações principais do FastAPI
from fastapi import FastAPI, WebSocket, Request, Depends
from fastapi.staticfiles import StaticFiles

# Dependência pra pegar usuário logado (provavelmente checa sessão/cookie)
from app.dependencies import get_usuario_logado

# ORM e funções de banco
from sqlalchemy.orm import Session
from sqlalchemy import func

# Schemas e modelos
from app.schemas import SessoesJogoSchema
from fastapi.templating import Jinja2Templates
from app.models import SessoesJogo, SessionLocal, Usuario, get_db

# Respostas prontas do FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

# Libs padrão
import asyncio
import socket
import struct
import json

import threading
import webbrowser

# Cria a aplicação FastAPI
app = FastAPI()

# Configura os templates (usando Jinja2)
templates = Jinja2Templates(directory="app/static/templates")

# Inclui as rotas de autenticação (login, registro, etc)
app.include_router(rota_auth)


# Lista de conexões WebSocket ativas
clients = []

# Endereço e porta para o servidor UDP que recebe dados do jogo
UDP_IP = "127.0.0.1"
UDP_PORT = 5300

# Monta a pasta de arquivos estáticos (CSS, JS, imagens, etc)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def root():
    return RedirectResponse(url="/auth/login")

# ---------- ROTA WEBSOCKET ----------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Aceita a conexão do cliente
    await websocket.accept()
    clients.append(websocket)
    
    try:
        # Mantém a conexão aberta indefinidamente
        while True:
            await asyncio.sleep(1)
    except:
        # Remove cliente se desconectar
        clients.remove(websocket)


# ---------- EVENTO DE STARTUP ----------
@app.on_event("startup")
async def startup_event():
    try:
        # Cria uma task assíncrona pra escutar pacotes UDP do jogo
        asyncio.create_task(upd_listener())
        
        # Abre o navegador automaticamente no login quando o servidor inicia

        def open_browser():
            webbrowser.open_new("http://127.0.0.1:8000/auth/login")
        threading.Timer(1.5, open_browser).start()
        
    except Exception as e:
        print(f"Erro ao iniciar o UDP: {e}")


# ---------- FUNÇÃO PRA SALVAR NO BANCO ----------
def salvarDB(session: Session, dados: SessoesJogoSchema):
    try:
        # Cria um novo registro da sessão de jogo
        nova_sessao = SessoesJogo(
            Nome_carro=dados.Nome_Carro,
            Quantidade_volta=dados.Quantidade_volta,
            Tempo_volta=dados.Tempo_volta,
        )
        # Adiciona e confirma no banco
        session.add(nova_sessao)
        session.commit()
    except Exception as e:
        print(f"Erro ao salvar os dados: {e}")

# ---------- MAPEAMENTO DOS CARROS ----------
def buscar_carro(carroID):
    carros = {
        2544:"VIPER 2016",
        1131:"458 2013",
        1599:"599XX E",
        2750:"Twin Mill",
        1670:"MP4 F1",
        338:"Mclaren F1 GT",
        2470:"Vulcan",
        3072:"911 GT3 2019",
        1175:"Pagani zonda r",
        631:"AM DBR9",
        2813:"DEMON FF",
        1011:"M3 2008",
        1111:"M3 GT2"
    }

    try:
        # Retorna o nome do carro, se existir
        if carroID in carros:
            return carros[carroID]
        else:
            return "Carro Desconhecido"
    except Exception as e:
        print(f"Erro ao achar o carro: {e}")

# ---------- CHECA SE A CORRIDA ESTÁ ATIVA ----------
def corridaStatus(isRaceOn):
    try:
        # 1 = corrida em andamento, 0 = parada
        if isRaceOn:
            return True
        else:
            return False
    except Exception as e:
        print(f"Erro: {e}")


# ---------- OUVINTE UDP (CORAÇÃO DO SISTEMA) ----------
async def upd_listener():
    # Cria o socket UDP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        sock.setblocking(False)
        bestlapOLD = None  # Guarda o último tempo de volta salvo

    except Exception as e:
        print(f"Erro ao conectar: {e}")

    while True:
        try:
            # Recebe dados do jogo
            data, addr = sock.recvfrom(4096)
            # Se o pacote for muito pequeno, ignora
            if len(data) < 228:
                print("Pacote muito pequeno, aguardando próximo...")
                continue
        except BlockingIOError:
            # Se não houver dados ainda, espera um pouco e tenta de novo
            await asyncio.sleep(0.01)
            continue
            
        try:
            # Extrai dados binários do pacote (offsets específicos)
            current_rpm = struct.unpack_from('<f', data, 16)[0]
            gear = struct.unpack_from('<B', data, 307)[0]
            steer = struct.unpack_from('<b', data, 308)[0]
            acelerador = struct.unpack_from('<B', data, 303)[0]
            freio = struct.unpack_from('<B', data, 304)[0]
            velocidade = struct.unpack_from('<f', data, 244)[0]
            boost = struct.unpack_from('<f', data, 272)[0]
            bestlap = struct.unpack_from('<f', data, 284)[0]
            racePosition = struct.unpack_from('<B', data, 302)[0]
            lapNumber = struct.unpack_from('<h', data, 300)[0]
            fuel = struct.unpack_from('<f', data, 276)[0]
            isRaceOn = struct.unpack_from('<i', data, 0)[0]
            corridastatus = corridaStatus(isRaceOn)
            carroID = struct.unpack_from('<i', data, 212)[0]
            carro = buscar_carro(carroID)
            
            # Se tiver dados válidos, cria o schema e salva no banco
            if carro and bestlap and lapNumber != 0:
                dados = SessoesJogoSchema(
                    Nome_Carro = carro,
                    Quantidade_volta = lapNumber,
                    Tempo_volta = bestlap
                )
                with SessionLocal() as session:
                    # Só salva se for uma nova melhor volta
                    if bestlapOLD != bestlap:
                        salvarDB(session, dados)
                        bestlapOLD = bestlap
                   
            # Monta mensagem pra enviar via WebSocket
            msg = json.dumps({
                "rpm": current_rpm,
                "gear": gear,
                "steer": steer,
                "acelerador": round(acelerador / 255 * 100),
                "freio": round(freio / 255 * 100),
                "velocidade": round(velocidade * 3.6, 1),
                "boost": round(boost / 14.504, 2),
                "bestlap": float(round(bestlap, 2)),
                "racePosition": racePosition,
                "lapNumber": lapNumber,
                "fuel": round(fuel / 1 * 100),
                "carro": carro,
                "corridastatus": corridastatus,
            })

            # Envia dados pra todos os clientes conectados
            for client in clients:
                await client.send_text(msg)

        except struct.error as e:
            print(f"Erro ao decodificar pacote: {e}")


# ---------- ROTA: HISTÓRICO DE TEMPOS ----------
@app.get("/historico", response_class=HTMLResponse)
async def historico(request: Request, db: Session = Depends(get_db)):
    # Busca o melhor tempo de cada carro no banco
    melhores_tempos = db.query(
        SessoesJogo.Nome_carro,
        func.min(SessoesJogo.Tempo_volta).label("melhor_tempo")
    ).group_by(SessoesJogo.Nome_carro).all()

    # Renderiza o template
    return templates.TemplateResponse("historico.html", {"request": request, "dados": melhores_tempos})


# ---------- ROTA: DASHBOARD ----------
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Abre o dashboard principal
    with SessionLocal() as session:
        return templates.TemplateResponse("dashboard.html", {"request": request})


# ---------- ROTA: PERFIL DO USUÁRIO ----------
@app.get("/perfil", response_class=HTMLResponse)
async def perfil(request: Request, usuario: Usuario = Depends(get_usuario_logado)):
    # Se o usuário não estiver logado, redireciona pro login
    if not usuario:
        return RedirectResponse("/auth/login")

    # Renderiza o perfil com os dados do usuário
    return templates.TemplateResponse("perfil.html", {"request": request, "usuario": usuario})
