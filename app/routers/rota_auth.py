# Imports principais
from fastapi import APIRouter, HTTPException, Depends
from app.models import Usuario, get_db
from passlib.context import CryptContext  # para hash de senha
from fastapi import Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.schemas import LoginSchema, RegistroSchema
from pydantic import ValidationError

# Configura o bcrypt como método de hash
bcrypt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria o router da parte de autenticação
rota_auth = APIRouter(prefix="/auth", tags=["auth"])

# Define onde ficam os templates HTML
templates = Jinja2Templates(directory="app/static/templates")


# ------------------- REGISTRO -------------------
@rota_auth.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    # Retorna o template de registro (formulário)
    return templates.TemplateResponse("register.html", {"request": request})
    

@rota_auth.post("/register")
async def post_register(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    # Valida os dados usando Pydantic
    try:
        registro = RegistroSchema(nome=nome, email=email, senha=senha)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    
    try:
        # Faz hash da senha antes de salvar
        senha_hash = bcrypt.hash(registro.senha)

        # Cria o usuário no banco
        usuario = Usuario(nome=registro.nome, email=registro.email, senha=senha_hash)
        db.add(usuario)
        db.commit()

        # Redireciona pro login
        return RedirectResponse("/auth/login", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno, tente novamente mais tarde")


# ------------------- LOGIN -------------------
@rota_auth.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    # Retorna o template de login
    return templates.TemplateResponse("index.html", {"request": request})


@rota_auth.post("/login")
async def post_login(
    login: LoginSchema = Depends(LoginSchema.as_form),  # Pega os dados via form
    db: Session = Depends(get_db)
):
    try:
        # Procura usuário pelo email
        usuario = db.query(Usuario).filter(Usuario.email == login.email).first()
        if not usuario:
            raise HTTPException(status_code=400, detail="Usuario não encontrado")

        # Verifica se a senha bate
        if not bcrypt.verify(login.senha, usuario.senha):
            raise HTTPException(status_code=400, detail="Email ou Senha incorretos")

        # Cria a resposta redirecionando pro histórico
        response = RedirectResponse("/historico", status_code=303)

        # Define o cookie 'usuario_id' com o id do usuário logado
        # É exatamente esse cookie que o get_usuario_logado() usa
        response.set_cookie(key="usuario_id", value=str(usuario.id))
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno, tente novamente mais tarde")
