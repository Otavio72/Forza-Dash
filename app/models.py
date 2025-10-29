# Importa módulos do SQLAlchemy que servem para criar e configurar o banco de dados e suas tabelas
from sqlalchemy import create_engine, Column, Integer, Boolean, Float, String, UniqueConstraint 
from sqlalchemy.orm import declarative_base, sessionmaker

# Cria uma conexão (engine) com o banco de dados SQLite chamado "banco.db"
# O "sqlite:///" indica o caminho local (sem servidor)
db = create_engine(
    "sqlite:///banco.db"
)

# Cria uma fábrica de sessões — basicamente, o “controle remoto” que a aplicação usa pra conversar com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db)

# Cria uma classe base que serve como molde pra todos os modelos (tabelas) do SQLAlchemy
Base = declarative_base()

# Função geradora pra obter uma sessão de banco de dados
# Ela garante que, ao final do uso, a conexão é fechada corretamente (boa prática no FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Modelo (tabela) de usuários
class Usuario(Base):
    __tablename__ = "usuarios"    # Nome da tabela no banco

    # Colunas da tabela
    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False)
    nome = Column("nome", String(100))
    email = Column("email", String(100), nullable=False)
    senha = Column("senha", String(200))
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)  # Define se o usuário é admin

# Modelo (tabela) das sessões de jogo (dados de gameplay)
class SessoesJogo(Base):
    __tablename__= "SessoesJogo"  # Nome da tabela

    # Colunas da tabela
    id = Column("id", Integer, autoincrement=True, primary_key=True, nullable=False)
    Tempo_volta = Column("Tempo_volta", Float)  # Tempo de volta do carro
    Quantidade_volta = Column("Quantidade_volta", Integer)  # Quantidade de voltas
    Nome_carro = Column("Nome_carro", String(100))  # Nome do carro usado

    # Construtor pra facilitar a criação de instâncias dessa classe
    def __init__(self, Tempo_volta, Quantidade_volta, Nome_carro):
        self.Quantidade_volta = Quantidade_volta
        self.Tempo_volta = Tempo_volta
        self.Nome_carro = Nome_carro

    # Define uma restrição única (unique constraint)
    # Garante que não existam dois registros com o mesmo tempo e nome de carro
    __table_args__ = (
        UniqueConstraint("Tempo_volta", "Nome_carro", name="uix_tempo_carro"),
    )
