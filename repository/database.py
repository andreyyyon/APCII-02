from sqlalchemy import (
    create_engine, Column, String, Integer, Boolean, Enum, DateTime,
    ForeignKey, CheckConstraint, func
)
from sqlalchemy.orm import declarative_base, relationship, Session
from datetime import datetime, timezone

# ==========================================================
# CONFIGURAÇÃO DO BANCO
# ==========================================================

# Cria o arquivo SQLite localmente
URL_BANCO = "sqlite:///estacionamento.db"

# Engine = “motor” de conexão com o banco
engine = create_engine(URL_BANCO, echo=False, future=True)

# Base das classes ORM (tabelas)
Base = declarative_base()

# ==========================================================
# MODELOS (TABELAS)
# ==========================================================

class Vaga(Base):
    __tablename__ = "vagas"

    codigo = Column(String, primary_key=True)  # Ex: M101
    tipo = Column(Enum("M", "G", "C", "E", name="tipo_vaga"), nullable=False)
    ocupada = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Vaga(codigo={self.codigo}, tipo={self.tipo}, ocupada={self.ocupada})>"


class Veiculo(Base):
    __tablename__ = "veiculos"

    placa = Column(String, primary_key=True)
    modelo = Column(String, nullable=False)
    cor = Column(String, nullable=False)
    tipo = Column(Enum("C", "M", name="tipo_veiculo"), nullable=False)
    tamanho = Column(Enum("M", "G", name="tamanho_carro"), nullable=True)
    eletrica = Column(Boolean, nullable=True)
    vaga_atual = Column(String, ForeignKey("vagas.codigo"), nullable=True)

    estadias = relationship("Estadia", back_populates="veiculo")
    vaga_rel = relationship("Vaga", foreign_keys=[vaga_atual])

    __table_args__ = (
        CheckConstraint(
            "(tipo='C' AND tamanho IS NOT NULL AND eletrica IS NULL) OR "
            "(tipo='M' AND tamanho IS NULL AND eletrica IS NOT NULL)",
            name="ck_veiculo_integridade"
        ),
    )

    def __repr__(self):
        return f"<Veiculo(placa={self.placa}, tipo={self.tipo})>"


class Estadia(Base):
    __tablename__ = "estadias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    placa = Column(String, ForeignKey("veiculos.placa"), nullable=False)
    vaga = Column(String, ForeignKey("vagas.codigo"), nullable=False)
    entrada = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    saida = Column(DateTime(timezone=True), nullable=True)

    veiculo = relationship("Veiculo", back_populates="estadias")
    vaga_rel = relationship("Vaga", foreign_keys=[vaga])

    __table_args__ = (
        CheckConstraint("saida IS NULL OR saida >= entrada", name="ck_estadia_ordem_temporal"),
    )

    def __repr__(self):
        return f"<Estadia(placa={self.placa}, vaga={self.vaga}, entrada={self.entrada}, saida={self.saida})>"


# FUNÇÕES AUXILIARES

def iniciar_banco():
    """Cria as tabelas e cadastra as vagas iniciais (M/G/C/E de 101 a 125)."""
    Base.metadata.create_all(bind=engine)

    sessao = Session(bind=engine)

    quantidade = sessao.query(Vaga).count()
    if quantidade == 0:
        tipos = ["M", "G", "C", "E"]
        for tipo in tipos:
            for numero in range(101, 126):
                codigo = f"{tipo}{numero}"
                nova_vaga = Vaga(codigo=codigo, tipo=tipo, ocupada=False)
                sessao.add(nova_vaga)
        sessao.commit()
        print("✅ Vagas iniciais criadas com sucesso.")
    else:
        print(f"Banco já possui {quantidade} vagas cadastradas.")

    sessao.close()


def conectar():
    """Cria uma sessão de conexão com o banco (você usa nas funções depois)."""
    return Session(bind=engine)