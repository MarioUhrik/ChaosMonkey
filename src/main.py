import time
import os
import logging

from kubernetes import client, config

def chaosMonkey(config):
    while True:
        logging.debug("Listing pods in namespace " + config["targetNamespace"])
        pods = config["k8sApi"].list_namespaced_pod(config["targetNamespace"])
        logging.debug("Found pods: " + pods)
        if len(pods.items) == 0:
            logging.warning("Found zero pods in namespace" + config["targetNamespace")
        else:
            podToDelete = pods.items[randrange(len(pods.items))].metadata.name
            logging.debug("Deleting pod " + podToDelete)
            config["k8sApi"].delete_namespaced_pod(config["targetNamespace"], podToDelete)
            logging.info("Deleted pod " + podToDelete)

        logging.debug("Sleeping for " + config["interval"] + " seconds")
        time.sleep(config["interval"])

def init():
    logLevel = os.environ.get('CM__LOGLEVEL', 'INFO').upper()
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logLevel)
    logging.info("Initializing...")

    config = {}
    config["interval"] = os.getenv('CM__INTERVAL')
    if config["interval"] is None:
        raise Exception("Init failure: CM__INTERVAL env variable could not be loaded")

    config["targetNamespace"] = os.getenv('CM__TARGET_NAMESPACE')
    if config["targetNamespace"] is None:
        raise Exception("Init failure: CM__TARGET_NAMESPACE env variable could not be loaded")

    kubernetes.config.load_kube_config()
    config["k8sApi"] = kubernetes.client.CoreV1Api()

    logging.info("Initialized!")
    return config

def main():
    config = init()
    chaosMonkey(config)

if __name__ == '__main__':
    main()
