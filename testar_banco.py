from repository.database import iniciar_banco, FabricaSessao, Vaga

iniciar_banco()

with FabricaSessao() as s:
    livres = s.query(Vaga).filter_by(ocupada=False).order_by(Vaga.codigo).limit(5).all()
    for v in livres:
        print(v)