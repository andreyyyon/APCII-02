# Definindo escopo global de armazenamento

registro_entrada = []
clientes = []
vagas = []
estadias = []

# Carro Médio (M)
for i in range(1, 26):
    vagas.append(f"M{100+i}")

# Carro Grande (G)
for i in range(1, 26):
    vagas.append(f"G{100+i}")

# Moto Combustão (C)
for i in range(1, 26):
    vagas.append(f"C{100+i}")

# Moto Elétrica (E)
for i in range(1, 26):
    vagas.append(f"E{100+i}")