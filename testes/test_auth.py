# testes/test_auth.py
# -----------------------------------------------------------
# 📄 Testes automatizados para autenticação e registro de usuários.
# Aqui validamos os fluxos de:
#  - Login com sucesso e falhas (senha incorreta, e-mail inválido)
#  - Registro de novos usuários
# -----------------------------------------------------------

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt
from app.main import app 
from app.models import Base, Usuario, get_db


# ===========================================================
# 🔧 Configuração do banco de dados em memória (SQLite)
# ===========================================================
# Cada teste roda isoladamente com um banco descartável,
# garantindo integridade e independência dos testes.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas baseadas no modelo da aplicação
Base.metadata.create_all(bind=engine)


# ===========================================================
# 🧪 Fixtures do Pytest
# ===========================================================

@pytest.fixture()
def db_session():
    """Cria uma sessão temporária de banco de dados para cada teste."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    """
    Substitui a dependência original de banco de dados pela de teste.
    Isso garante que o app use a sessão de teste durante cada execução.
    """
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()


# ===========================================================
# 🔐 Testes de Login
# ===========================================================

@pytest.mark.asyncio
async def test_login_sucesso(db_session):
    """
    ✅ Cenário de sucesso:
    Usuário faz login com e-mail e senha corretos.
    Espera-se redirecionamento (303) e cookie de sessão definido.
    """

    senha = "1234"
    senha_hashed = bcrypt.hash(senha)
    usuario = Usuario(email="teste@email.com", senha=senha_hashed)
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "email": "teste@email.com",
                "senha": "1234"
            }
        )

    assert response.status_code == 303  # Redirecionamento OK
    assert f"usuario_id={usuario.id}" in response.headers.get("set-cookie", "")


@pytest.mark.asyncio
async def test_login_falha_senha(db_session):
    """
    ❌ Cenário de falha:
    E-mail correto, mas senha incorreta.
    Deve retornar erro 422 (Unprocessable Entity).
    """

    senha = "123"
    senha_hashed = bcrypt.hash(senha)

    usuario = Usuario(email="teste@email.com", senha=senha_hashed)
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "usuario_Email": "teste@email.com",  # Campos incorretos para simular erro
                "usuario_Senha": "123"
            }
        )

    assert response.status_code == 422
    assert f"usuario_id={usuario.id}" not in (response.headers.get("set-cookie") or "")


@pytest.mark.asyncio
async def test_login_falha_email(db_session):
    """
    ❌ Cenário de falha:
    E-mail incorreto (não existe no banco).
    Deve retornar 422 e não definir cookie de sessão.
    """

    senha = "1234"
    senha_hashed = bcrypt.hash(senha)

    usuario = Usuario(email="EmailDeverasErrado", senha=senha_hashed)
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post(
            "/auth/login",
            data={
                "usuario_Email": "teste@email.com",
                "usuario_Senha": "1234"
            }
        )

    assert response.status_code == 422
    assert f"usuario_id={usuario.id}" not in (response.headers.get("set-cookie") or "")


# ===========================================================
# 🧾 Testes de Registro
# ===========================================================

@pytest.mark.asyncio
async def test_registro_sucesso(db_session):
    """
    ✅ Cenário de sucesso:
    Registro de um novo usuário com dados válidos.
    Espera-se redirecionamento (303).
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post(
            "/auth/register",
            data={
                "nome": "Teste",
                "email": "teste@email.com",
                "senha": "1234"
            }
        )

    assert response.status_code == 303


@pytest.mark.asyncio
async def test_registro_falha(db_session):
    """
    ❌ Cenário de falha:
    Dados inválidos (nome curto, e-mail incorreto e senha fraca).
    Deve retornar erro 422.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.post(
            "/auth/register",
            data={
                "nome": "Te",                # Muito curto
                "email": "testeemailcom",    # Sem '@'
                "senha": "12"                # Fraca
            }
        )

    assert response.status_code == 422
