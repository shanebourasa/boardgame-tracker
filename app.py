from flask import Flask, render_template

app = Flask(__name__)

game_data = {}

@app.route('/')
def hello_world(name='shane'):
    return render_template('hello.html', person=name)

@app.route('/games')
def game_list():
    return render_template('games.html')

if __name__ == "__main__":
    app.run(debug=True)