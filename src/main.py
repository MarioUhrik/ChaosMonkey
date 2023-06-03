import time
import os
import random
import logging
from kubernetes import client, config

def chaosMonkey(settings):
    while True:
        logging.info("Listing pods in namespace " + settings["targetNamespace"])
        pods = settings["k8sApi"].list_namespaced_pod(settings["targetNamespace"])
        if len(pods.items) == 0:
            logging.warning("Found zero pods in namespace" + settings["targetNamespace"])
        else:
            podToDelete = pods.items[random.randrange(len(pods.items))].metadata.name
            logging.debug("Deleting pod " + podToDelete)
            settings["k8sApi"].delete_namespaced_pod(podToDelete, settings["targetNamespace"])
            logging.info("Deleted pod " + podToDelete)

        logging.debug("Sleeping for " + settings["interval"] + " seconds")
        time.sleep(settings["interval"])

def init():
    logLevel = os.environ.get('CM__LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logLevel)
    logging.info("Initializing...")

    settings = {}
    settings["interval"] = os.getenv('CM__INTERVAL')
    if settings["interval"] is None:
        raise Exception("Init failure: CM__INTERVAL env variable could not be loaded")

    settings["targetNamespace"] = os.getenv('CM__TARGET_NAMESPACE')
    if settings["targetNamespace"] is None:
        raise Exception("Init failure: CM__TARGET_NAMESPACE env variable could not be loaded")

    config.load_incluster_config()
    settings["k8sApi"] = client.CoreV1Api()

    logging.info("Initialized!")
    return settings


chaosMonkey(init())
