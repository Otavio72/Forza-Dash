# testes/test_historico.py
# -----------------------------------------------------------
# 📄 Teste automatizado para o endpoint /historico.
# O objetivo é garantir que o histórico de sessões (voltas)
# seja exibido corretamente na interface do usuário.
# -----------------------------------------------------------

import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app  
from app.models import Base, SessoesJogo, get_db


# ===========================================================
# 🔧 Configuração do banco de dados temporário (SQLite em memória)
# ===========================================================
# Cada teste roda num banco isolado e descartável,
# garantindo independência total entre os testes.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria as tabelas baseadas no modelo da aplicação
Base.metadata.create_all(bind=engine)


# ===========================================================
# 🧪 Fixtures do Pytest
# ===========================================================

@pytest.fixture()
def db_session():
    """Cria e fornece uma sessão de banco de dados temporária para o teste."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# ===========================================================
# 🧩 Teste principal: histórico de sessões do jogo
# ===========================================================
@pytest.mark.asyncio
async def test_historico_sucesso(db_session):
    """
    Verifica se o endpoint /historico retorna corretamente os dados
    das sessões de jogo armazenadas no banco.
    """

    # Simula uma sessão de jogo salva no banco
    Nome_carro = "M3 GT2"
    Quantidade_volta = "5"
    Tempo_volta = "25.90810394287109"

    nova_sessao = SessoesJogo(
        Nome_carro=Nome_carro,
        Quantidade_volta=Quantidade_volta,
        Tempo_volta=Tempo_volta,
    )
    db_session.add(nova_sessao)
    db_session.commit()

    # Substitui a dependência de DB original pela de teste
    app.dependency_overrides[get_db] = lambda: db_session

    # Usa transporte ASGI pra simular requisições HTTP reais
    transport = ASGITransport(app=app)

    # Faz a requisição GET para o endpoint /historico
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/historico")

    # ======================
    # ✅ Verificações finais
    # ======================
    assert response.status_code == 200               # Página carregou com sucesso

    html = response.text
    assert "M3 GT2" in html                          # O nome do carro aparece no HTML
    assert "25.91 s" in html                         # O tempo aparece formatado corretamente

    # Limpa overrides de dependências
    app.dependency_overrides.clear()
