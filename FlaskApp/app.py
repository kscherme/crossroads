#!/usr/bin python
from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

if __name__ == "__main__":
	app.run(host='dsg1.crc.nd.edu',port=5200)

#help

