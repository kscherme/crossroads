#!/usr/bin python
from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def main():
	return render_template('index.html')

<<<<<<< HEAD
if __name__ == "__main__":
	app.run(host='dsg1.crc.nd.edu',port=5200)
=======
# if __name__ == "__main__":
# 	app.run()
>>>>>>> 77f0c3dae6050e8ae2c751197e2014dcb16d1698

#help

