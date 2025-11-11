from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Rota Principal: Home / Registrar Entrada/Saída
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        # Aqui ficará a lógica de ENTRADA/SAÍDA (BD)
        mensagem = None # Inicializa a mensagem (apenas estética)
        
        # Simulação de feedback (apenas estético, sem BD)
        if placa:
            mensagem = f"Placa {placa} processada. Aguardando lógica de ENTRADA/SAÍDA."
            return render_template('index.html', mensagem=mensagem)
    
    return render_template('index.html', mensagem=None)

# Rota para Listar Clientes
@app.route('/clientes')
def listar_clientes():
    # Aqui ficará a busca de todos os clientes no BD
    clientes = [] # Lista vazia, conforme solicitado
    return render_template('clientes.html', clientes=clientes)

# Rota para Consultar Estadias
@app.route('/estadias', methods=['GET', 'POST'])
def consultar_estadias():
    placa_buscada = None
    estadias = []
    
    if request.method == 'POST':
        placa_buscada = request.form.get('placa').strip().upper()
        # Aqui ficará a lógica de busca de estadias no BD
        
    return render_template('consultar_estadias.html', placa_buscada=placa_buscada, estadias=estadias)

if __name__ == '__main__':
    app.run(debug=True)