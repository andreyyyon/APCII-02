# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from repository.database import iniciar_banco
from repository.estacionamento_repo import processar_placa

app = Flask(__name__)
app.secret_key = "troque-esta-chave"
iniciar_banco()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # Exibe o formulário de entrada
        return render_template("index.html")

    # Se for POST, processa a placa digitada
    placa = request.form.get("input_placa", "").strip()
    if not placa:
        flash("Por favor, informe a placa do veículo.", "error")
        return redirect(url_for("index"))

    try:
        resultado = processar_placa(placa)
        acao = resultado["acao"]

        if acao == "registrar_cliente":
            # Se a placa ainda não existe, redireciona para a página de cadastro
            return redirect(url_for("registrar_cliente", placa=resultado["placa"]))

        elif acao == "registrar_saida":
            flash(f"Saída registrada para {resultado['placa']} (vaga {resultado['vaga']}).", "success")
            return redirect(url_for("index"))

        elif acao == "registrar_entrada":
            flash(f"Entrada registrada para {resultado['placa']} (vaga {resultado['vaga']}).", "success")
            return redirect(url_for("index"))

        else:
            flash("Ação desconhecida.", "error")
            return redirect(url_for("index"))

    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("index"))


@app.get("/registrar_cliente")
def registrar_cliente():
    # Aqui renderiza o formulário de cadastro de novo cliente
    return render_template("registrar_cliente.html", placa=request.args.get("placa", ""))


if __name__ == "__main__":
    app.run(debug=True)
