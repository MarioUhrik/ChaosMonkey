# ChaosMonkey

ChaosMonkey runs as a pod in your Kubernetes cluster, and deletes a random pod in namespace **targetNamespace** every **interval** seconds.

### Test running ChaosMonkey
```bash
minikube start # if you don't have your own cluster prepared, you can use minikube

kubectl apply -f manifests/chaosMonkey.yaml # deploy ChaosMonkey
kubectl apply -f manifests/dummyTargetNamespace.yaml # dummy namespace/pods in namespace `chaos`

kubectl -n chaos-monkey get pod # ensure that the ChaosMonkey deployment is ready
kubectl -n chaos get pod # ensure that the dummy pods are ready
kubectl -n chaos-monkey logs -l app=chaos-monkey -f # watch the logs of the ChaosMonkey pod
kubectl -n chaos get pod -w # watch the pods of the `chaos` namespace as they die

#cleanup
kubectl delete -f manifests/dummyTargetNamespace.yaml
kubectl delete -f manifests/chaosMonkey.yaml
minikube delete # if you've used `minikube start` up above
```

In order to run ChaosMonkey for non-testing purposes, you can edit the environment variables in `manifests/chaosMonkey.yaml` to your satisfaction, and then deploy it without the `dummyTargetNamespace.yaml`.
