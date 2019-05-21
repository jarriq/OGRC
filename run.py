from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/painel')
def painel():
    return render_template('painel.html')




if __name__=="__main__":
    app.run()
