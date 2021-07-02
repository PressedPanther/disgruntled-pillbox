from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', defaults={'path':''})
def home():
    return render_template('home.html')

@app.route('/',defaults={'path':''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file('home.html')

@app.route('/showcase/')
def showcase():
    return render_template('showcase.html')

@app.route('/stream/')
def stream():
    return render_template('stream.html')

if __name__ == '__main__':
    app.run(debug=True)