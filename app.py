import sqlite3

def init_db():
    conn = sqlite3.connect('imc.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pessoas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            peso REAL NOT NULL,
            altura REAL NOT NULL,
            imc REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inicializar o banco de dados
init_db()

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Função para calcular o IMC
def calcular_imc(peso, altura):
    imc = peso / (altura ** 2)
    if imc < 18.5:
        status = 'Abaixo do peso'
    elif 18.5 <= imc <= 24.9:
        status = 'Peso normal'
    elif 25 <= imc <= 29.9:
        status = 'Acima do peso'
    else:
        status = 'Obesidade'
    return round(imc, 2), status

# Função para armazenar os dados no banco de dados
def armazenar_dados(nome, peso, altura, imc, status):
    conn = sqlite3.connect('imc.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO pessoas (nome, peso, altura, imc, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (nome, peso, altura, imc, status))
    conn.commit()
    conn.close()

# Página inicial com o formulário
@app.route('/')
def index():
    return render_template('index.html')

# Rota para calcular o IMC e armazenar os dados
@app.route('/calcular', methods=['POST'])
def calcular():
    nome = request.form['nome']
    peso = float(request.form['peso'])
    altura = float(request.form['altura'])
    imc, status = calcular_imc(peso, altura)
    armazenar_dados(nome, peso, altura, imc, status)
    return render_template('resultado.html', nome=nome, imc=imc, status=status)

# Rota para exibir os dados do banco de dados
@app.route('/listar')
def listar():
    conn = sqlite3.connect('imc.db')
    c = conn.cursor()
    c.execute('SELECT nome, peso, altura, imc, status FROM pessoas')
    pessoas = c.fetchall()
    conn.close()
    return render_template('listar.html', pessoas=pessoas)

if __name__ == '__main__':
    app.run(debug=True)

