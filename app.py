from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
  return 'yolo'

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
