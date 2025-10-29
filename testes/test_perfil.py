# testes/test_auth.py
# -----------------------------------------------------------
# 📄 Teste automatizado para o módulo de autenticação do app.
# O objetivo é validar o fluxo de acesso à página de perfil,
# garantindo que o sistema retorne corretamente os dados do
# usuário autenticado.
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
# 🔧 Configuração do banco de dados temporário (em memória)
# ===========================================================
# Aqui criamos um SQLite apenas em memória — rápido e isolado —
# ideal para rodar testes sem afetar o banco real.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria todas as tabelas definidas no modelo para uso nos testes
Base.metadata.create_all(bind=engine)


# ===========================================================
# 🧪 Fixtures do Pytest
# ===========================================================
# Criam o ambiente de teste e controlam a sessão com o banco

@pytest.fixture()
def db_session():
    """Cria uma sessão de banco de dados temporária para cada teste."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def override_get_db(db_session):
    """Substitui a dependência original de get_db pelo banco de teste."""
    app.dependency_overrides[get_db] = lambda: db_session
    yield
    app.dependency_overrides.clear()


# ===========================================================
# 🧩 Teste principal: acesso ao perfil do usuário
# ===========================================================
@pytest.mark.asyncio
async def test_perfil_sucesso(db_session):
    """
    Verifica se o endpoint /perfil exibe corretamente os dados
    do usuário logado quando o cookie de autenticação é válido.
    """

    # Simula um usuário real com senha criptografada
    senha = "1234"
    senha_hashed = bcrypt.hash(senha)
    usuario = Usuario(email="teste@email.com", senha=senha_hashed, nome="testNome")

    # Adiciona o usuário no banco temporário
    db_session.add(usuario)
    db_session.commit()
    db_session.refresh(usuario)

    # Garante que a aplicação use o DB de teste
    app.dependency_overrides[get_db] = lambda: db_session

    # Configura o transporte ASGI para simular requisições HTTP reais
    transport = ASGITransport(app=app)

    # Executa uma requisição GET para o endpoint /perfil
    # simulando o cookie de autenticação do usuário
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/perfil", cookies={"usuario_id": str(usuario.id)})

    # ======================
    # ✅ Verificações finais
    # ======================
    assert response.status_code == 200  # Página carregou com sucesso

    html = response.text
    assert "testNome" in html           # Nome exibido corretamente
    assert "teste@email.com" in html    # Email exibido corretamente

    # Limpa overrides de dependência
    app.dependency_overrides.clear()
