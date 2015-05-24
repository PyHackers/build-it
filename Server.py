from flask import Flask
from docker import Client
import configparser
import json
import os
import zipfile

CONF_FILE = "/home/likewise-open/ZOHOCORP/tarun-2215/workspace/comp/devops/buildit.cfg"

SERVER_CONFIG = configparser.RawConfigParser()

SERVER_CONFIG.read(CONF_FILE)

app = Flask(__name__)

@app.route("/")
def hello():
	return "Hello World"

@app.route("/upload")
def upload():
	#fileUnzipper(file)
	cli = Client('unix://var/run/docker.sock')
	containers = cli.containers()
	images = cli.images()
	pContID = SERVER_CONFIG.get('PRIMARY_CONTAINER','id')
	pCmnd = SERVER_CONFIG.get('PRIMARY_CONTAINER','command')
	sContID = SERVER_CONFIG.get('SECONDARY_CONTAINER','id')
	for container in containers:
		if container["Id"] == pContID:
			createdCont = cli.create_container(image=container["Image"], command=str(pCmnd), tty=True)
			response = cli.start(container=createdCont.get('Id'))
			sContID = str(createdCont.get('Id'))
			print " Started copy of primary container " + str(createdCont.get('Id')) + " Now going to redirect traffic! "
			continue
	#redirecSecTraffic()
	#scriptExecutor(pContID)
	#redirecPriTraffic()
	print " Stopping and removing secondary container created "
	cli.stop(sContID)
	remRsp = cli.remove_container(sContID, force=True)
	print str(remRsp)
	return "Hello World" + str("\n")  + str(containers) + str(pContID) + str(sContID) + str(response)

def scriptExecutor(pContID):
	destPath = SERVER_CONFIG.get('BUILD_DETAILS','path')
	print " Going to execute script and update build in primary "
	out = os.system("sh extract.sh " +  str(pContID) +  " " + str(destPath))
	return out

def fileUnzipper(file):
	print " Unzipping files recieved in current directory in host "
	zf = zipfile.ZipFile(file)
	zf.extractall("../data/")

def redirectSecTraffic():
	pass

def removeContainer():
	print " Stopping and removing secondary container created "


def redirectPriTraffic():
	pass

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
