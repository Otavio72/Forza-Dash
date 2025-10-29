# Importa o engine do banco definido em models.py
from app.models import db

# Importa o sessionmaker (pra criar sessões do banco) e Session (tipo da sessão)
from sqlalchemy.orm import sessionmaker, Session

# Importa ferramentas do FastAPI: Cookie e Depends (injeção de dependências)
from fastapi import Cookie, Depends

# Importa o modelo de usuário e o get_db
from app.models import Usuario, get_db


# ---------- GERADOR DE SESSÃO DE BANCO ----------
def pegar_sessao():
    try:
        # Cria uma factory de sessão vinculada ao banco
        Session = sessionmaker(bind=db)
        session = Session()
        # "yield" permite usar o contexto dentro das rotas e fechar depois
        yield session
    finally:
        # Fecha a sessão ao final
        session.close()


# ---------- FUNÇÃO PRA PEGAR USUÁRIO LOGADO ----------
def get_usuario_logado(
    usuario_id: str | None = Cookie(None),  # pega o ID do usuário dos cookies
    db: Session = Depends(get_db)            # injeta a sessão do banco
):
    # Se não houver cookie, significa que o usuário não está logado
    if not usuario_id:
        return None

    # Busca o usuário no banco usando o ID armazenado no cookie
    return db.query(Usuario).filter(Usuario.id == int(usuario_id)).first()



        