# Importa o BaseModel (classe base do Pydantic), EmailStr (valida formato de e-mail)
# e constr (usado pra definir restrições em strings, tipo tamanho mínimo/máximo)
from pydantic import BaseModel, EmailStr, constr

# Importa Form, pra permitir que os dados sejam enviados via formulário HTML (não só JSON)
from fastapi import Form


# ---------- SCHEMA DE REGISTRO DE USUÁRIO ----------
class RegistroSchema(BaseModel):
    # Campos do formulário de registro com validações automáticas
    nome: constr(min_length=3)                      # mínimo de 3 caracteres
    email: EmailStr                                # valida se o texto é um e-mail válido
    senha: constr(min_length=4, max_length=72)     # senha entre 4 e 72 caracteres

    # Método que transforma esse schema em um "Form handler"
    # Isso permite usar o schema com formulários HTML via FastAPI (Form(...))
    @classmethod
    def as_form(
        cls,
        nome: str = Form(...),
        email: str = Form(...),
        senha: str = Form(...),
    ):
        # Cria uma instância do schema a partir dos dados do formulário
        return cls(nome=nome, email=email, senha=senha)
    

# ---------- SCHEMA DE LOGIN ----------
class LoginSchema(BaseModel):
    # Campos esperados pro login
    email: EmailStr
    senha: constr(min_length=4, max_length=72) 

    # Mesmo esquema do as_form pra receber dados vindos de formulários HTML
    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        senha: str = Form(...),
    ):
        return cls(email=email, senha=senha)


# ---------- SCHEMA DAS SESSÕES DE JOGO ----------
class SessoesJogoSchema(BaseModel):
    # Define o formato dos dados das sessões de jogo
    Tempo_volta: float
    Quantidade_volta: int
    Nome_Carro: str
