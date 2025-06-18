from flask import Flask, render_template, request, redirect, url_for, flash, session


app=Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':    
    app.run(debug=True)