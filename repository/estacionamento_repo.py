from datetime import datetime, timezone
from sqlalchemy.exc import IntegrityError
from .database import conectar, Vaga, Veiculo, Estadia

def _agora_utc():
    return datetime.now(timezone.utc)

def _tipo_vaga_para_veiculo(veiculo: Veiculo) -> str:
    """
    Retorna o tipo de vaga compatível com o veículo:
    - Carro: 'M' ou 'G' (usa Veiculo.tamanho)
    - Moto : 'E' se elétrica=True; senão 'C'
    """
    if veiculo.tipo == 'C':
        if veiculo.tamanho not in ('M', 'G'):
            raise ValueError("Para carros, o tamanho deve ser 'M' ou 'G'.")
        return veiculo.tamanho
    elif veiculo.tipo == 'M':
        if veiculo.eletrica is None:
            raise ValueError("Para motos, o atributo 'eletrica' é obrigatório.")
        return 'E' if veiculo.eletrica else 'C'
    else:
        raise ValueError("Tipo de veículo inválido. Use 'C' (carro) ou 'M' (moto).")

def _buscar_vaga_livre_por_tipo(sessao, tipo_vaga: str) -> Vaga | None:
    return (sessao.query(Vaga)
            .filter(Vaga.tipo == tipo_vaga, Vaga.ocupada == False)
            .order_by(Vaga.codigo.asc())
            .first())

def _registrar_saida(sessao, veiculo: Veiculo) -> dict:
    """Fecha a estadia aberta (se houver) e libera a vaga."""
    estadia = (sessao.query(Estadia)
               .filter(Estadia.placa == veiculo.placa, Estadia.saida.is_(None))
               .order_by(Estadia.id.desc())
               .first())
    if not estadia:
        raise ValueError("Não há estadia aberta para esta placa.")

    estadia.saida = _agora_utc()

    # Liberar a vaga ocupada
    if veiculo.vaga_atual:
        vaga = sessao.query(Vaga).get(veiculo.vaga_atual)
        if vaga:
            vaga.ocupada = False
    veiculo.vaga_atual = None

    sessao.commit()
    return {
        "acao": "registrar_saida",
        "placa": veiculo.placa,
        "vaga": estadia.vaga,
        "saida": estadia.saida
    }

def _registrar_entrada(sessao, veiculo: Veiculo) -> dict:
    """Abre uma nova estadia e ocupa uma vaga compatível."""
    tipo_vaga = _tipo_vaga_para_veiculo(veiculo)
    vaga = _buscar_vaga_livre_por_tipo(sessao, tipo_vaga)
    if not vaga:
        raise ValueError("Não há vagas disponíveis para este tipo de veículo.")

    vaga.ocupada = True
    veiculo.vaga_atual = vaga.codigo

    estadia = Estadia(
        placa=veiculo.placa,
        vaga=vaga.codigo,
        entrada=_agora_utc()
    )
    sessao.add(estadia)
    sessao.commit()

    return {
        "acao": "registrar_entrada",
        "placa": veiculo.placa,
        "vaga": vaga.codigo,
        "entrada": estadia.entrada
    }

def processar_placa(placa: str) -> dict:
    """
    Fluxo solicitado:
    1) Se a placa NÃO estiver cadastrada em 'veiculos' => retornar instrução para redirecionar.
    2) Se estiver cadastrada:
       2.1) Se houver estadia aberta => registrar SAÍDA, liberar vaga.
       2.2) Senão => registrar ENTRADA, ocupar vaga compatível.
    Retorna um dict com:
      - acao: 'registrar_cliente' | 'registrar_saida' | 'registrar_entrada'
      - dados extras conforme a ação (vaga, entrada/saida etc.)
    """
    sessao = conectar()
    try:
        p = placa.strip().upper()
        veiculo = sessao.query(Veiculo).get(p)

        if veiculo is None:
            # não cadastrado => redirecionar para a página de cadastro
            return {"acao": "registrar_cliente", "placa": p}

        # Verifica se já tem estadia aberta
        aberta = (sessao.query(Estadia)
                  .filter(Estadia.placa == p, Estadia.saida.is_(None))
                  .first())

        if aberta:
            return _registrar_saida(sessao, veiculo)
        else:
            return _registrar_entrada(sessao, veiculo)

    except IntegrityError as e:
        sessao.rollback()
        raise ValueError("Falha de integridade ao operar no banco.") from e
    except Exception:
        sessao.rollback()
        raise
    finally:
        sessao.close()