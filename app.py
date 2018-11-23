#!/usr/bin/env python3
import os
import uuid
import time
from kubernetes import client
from kubernetes.client import Configuration, ApiClient
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, session


# Initialize the Flask application
app = Flask(__name__)
app.secret_key = "SECRETYOUWILLNEVERGUESS"

@app.route('/')
def index():
    return render_template('index.html')

def create_namespaced_pod(namespace, pod_name, container_image):
	# General configuration (via kubectl proxy)
    myconfig=Configuration()
    myconfig.host = "127.0.0.1:8001"
    myapiclient = ApiClient(configuration=myconfig)
    v1 = client.CoreV1Api(api_client=myapiclient)

    # Check if pod already exists
    pod_list = v1.list_namespaced_pod(namespace)
    for pod in pod_list.items:
        if pod.metadata.name == pod_name:
        	# Pod exists
            return False

    # Pod definition
    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name=pod_name)
    # Container definition
    container = client.V1Container(name=pod_name)
    container.image = container_image
    container.args = ["sleep", "30"]
    container.name = pod_name
    # Pod spec
    spec = client.V1PodSpec(containers=container)
    spec.containers = [container]
    pod.spec = spec
    v1.create_namespaced_pod(namespace=namespace,body=pod)
    # Pod could be created
    return True


def check_running(namespace, pod_name):
    myconfig=Configuration()
    myconfig.host = "127.0.0.1:8001"
    myapiclient = ApiClient(configuration=myconfig)
    v1 = client.CoreV1Api(api_client=myapiclient)

    pod_list = v1.list_namespaced_pod(namespace)
    for pod in pod_list.items:
        if pod.metadata.name == pod_name:
            if pod.status.phase != "Running":
                print("Not running.")
                return False
            else:
                print("Running!")
                return True

@app.route('/create_pod')
def create_pod():
    
	if create_namespaced_pod("api-kube", "busybox", "busybox") != True:
		return "POD EXISTS."

    # List pods and get ip and status of newly created pod
    while check_running("api-kube", "busybox") != True:
        time.sleep(1)
    # RETURN MESSAGE
    return "CREATED POD."

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=4545, threaded=True)
