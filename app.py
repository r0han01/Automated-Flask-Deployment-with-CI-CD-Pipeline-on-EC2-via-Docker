from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    # Run Flask app on host 0.0.0.0 and port 9000
    app.run(host='0.0.0.0', port=9000, debug=True)
