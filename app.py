from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
  return render_template("index.html")


@app.route('/file', methods=['GET'])
def filePicker():
  return render_template("file.html")


@app.route('/aviary', methods=['GET'])
def aviary():
  return render_template("aviary.html")


@app.route('/upload', methods=['POST'])
def upload():
  print request.params['url']
  return 200

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.debug = True
  app.run(host='0.0.0.0', port=port)
