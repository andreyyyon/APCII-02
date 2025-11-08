from flask import Flask, render_template, request, redirect, url_for

# GitHub do professor Rogério: https://github.com/rogercodeeti

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)