from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Rota Principal: Exibe o formulário de Entrada/Saída. 
    Trata o POST do formulário de placa.
    """
    mensagem = request.args.get('mensagem_sucesso')
    
    if request.method == 'POST':
        placa = request.form.get('placa').strip().upper()
        
        placa_encontrada_no_bd = False 
        
        if not placa_encontrada_no_bd:
            mensagem = f"Placa {placa} não encontrada. Por favor, cadastre o veículo."
            return render_template('index.html', mensagem=mensagem, placa_nao_encontrada=placa)
        
        mensagem = f"Placa {placa} processada com sucesso!"
        
    return render_template('index.html', mensagem=mensagem)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """
    Rota de Cadastro: Lida com o formulário multipassos de cadastro.
    CORREÇÃO: O template chamado é 'cadastro.html'.
    """
    form_data = request.args.to_dict()
    step = int(form_data.get('step', 1))
    
    if request.method == 'POST':
        data = request.form.to_dict()
        next_step = step + 1 
        
        if step == 2:
            placa = data.get('placa')
            
            print(f"CADASTRO FINALIZADO: {data}")

            return redirect(url_for('home', mensagem_sucesso=f"Veículo {placa} cadastrado!"))

        args = {k: v for k, v in data.items() if v}
        args['step'] = next_step
        
        return redirect(url_for('cadastro', **args))
    
    return render_template('cadastro.html', 
                           step=step, 
                           form_data=form_data)

@app.route('/clientes')
def listar_clientes():
    """
    Rota de Clientes: Lista os clientes. 
    CORREÇÃO: O nome da função é 'listar_clientes'.
    """
    clientes = [
        {
            "placa": "123",
            "modelo": "HB20",
            "cor": "Preto",
            "tipo": "Carro",
            "vaga": "XYZ"
        }
    ] # Dados reais viriam do banco de dados
    return render_template('clientes.html', clientes=clientes) 

@app.route('/estadias')
def estadias():
    """
    Rota de Estadias: Exibe e consulta estadias.
    CORREÇÃO: Assumindo que o template correto é 'estadias.html'
    """
    return render_template('estadias.html') 


if __name__ == '__main__':
    app.run(debug=True)