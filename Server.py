from flask import Flask, request, jsonify
from docker import Client
import configparser
import json
import os
import zipfile

CONF_FILE = "./buildit.cfg"

SERVER_CONFIG = configparser.RawConfigParser()

SERVER_CONFIG.read(CONF_FILE)

app = Flask(__name__)

@app.route("/")
def hello():
	cli = Client('unix://var/run/docker.sock')
	containers = cli.containers()
	images = cli.images()
	pContID = SERVER_CONFIG.get('PRIMARY_CONTAINER','id')
	pCmnd = SERVER_CONFIG.get('PRIMARY_CONTAINER','command')
	sContID = SERVER_CONFIG.get('SECONDARY_CONTAINER','id')
	for container in containers:
		if container["Id"] == pContID:
			createdCont = cli.create_container(image=container["Image"], command=str(pCmnd))
			continue
	return "Hello World" + str("\n")  + str(containers) + str(pContID) + str(sContID) + str(createdCont)

@app.route('/uploadBuild', methods=['GET', 'POST'])
def uploadBuild():
	url = request.form.get('url')
	print "Url::"
	print url
	processBuild(url)
	return str(url)

def processBuild(url):

	return ""
	
def scriptExecutor(pContID):
	destPath = SERVER_CONFIG.get('BUILD_DETAILS','path')
	out = os.system("sh extract.sh " +  str(pContID) +  " " + str(destPath))
	return out

def fileUnzipper(file):
	zf = zipfile.ZipFile(file)
	zf.extractall("../data/")

def redirectTraffic():
	pass

def closeContainer():
	pass

def redirectTraffic():
	pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)