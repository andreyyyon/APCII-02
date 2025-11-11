from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# --- ROTAS PRINCIPAIS ---

@app.route('/', methods=['GET', 'POST'])
def home():
    mensagem = request.args.get('mensagem_sucesso')
    
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        
        placa_encontrada_no_bd = False 
        
        if not placa_encontrada_no_bd:
            return redirect(url_for('cadastro', placa_inicial=placa))
        
    return render_template('index.html', mensagem=mensagem)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        placa = request.form.get('placa')
        modelo = request.form.get('modelo')
        cor = request.form.get('cor')
        tipo = request.form.get('tipo') 
        tamanho = request.form.get('tamanho')
        eletrica = request.form.get('eletrica')
        
        # LOG de teste
        print(f"Cadastro recebido: {placa} ({tipo})")

        return redirect(url_for('home', mensagem_sucesso=f'Veículo {placa} cadastrado e entrada registrada!'))

    placa_inicial = request.args.get('placa_inicial')
    return render_template('registrar_veiculo.html', placa_inicial=placa_inicial)

# --- ROTAS DE NAVEGAÇÃO ---

@app.route('/clientes')
def listar_clientes():
    clientes = []
    return render_template('clientes.html', clientes=clientes) 

@app.route('/estadias')
def consultar_estadias():
    return render_template('consultar_estadias.html') 

if __name__ == '__main__':
    app.run(debug=True)