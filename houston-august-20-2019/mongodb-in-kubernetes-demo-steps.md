demo steps
===

This is a very simple test connecting a simple
Python app to MongoDB running in Kubernetes.

To start from scratch:

# Create a namespace
kubectl create ns mongodb

# Switch to that namespace
kubectl config set-context $(kubectl config current-context) --namespace mongodb

# (Enable kubectl command line completion)
source <(kubectl completion zsh)

# Create CRDS and Operator
kubectl apply -f https://raw.githubusercontent.com/mongodb/mongodb-enterprise-kubernetes/master/crds.yaml
kubectl apply -f https://raw.githubusercontent.com/mongodb/mongodb-enterprise-kubernetes/master/mongodb-enterprise.yaml

# Check pods and logs to see operator running smoothly
kubectl get pods
kubectl logs -f mongodb-...

# Create a ConfigMap for Cloud Mgr Project and Secret
kubectl apply -f mongodb-in-kubernetes-cloud-mgr-admin.yaml
kubectl apply -f mongodb-in-kubernetes-cloud-mgr-project.yaml

# Create a sample replica set
kubectl apply -f mongodb-in-kubernetes-replica-set.yaml


# Create the test
kubectl apply -f test.yaml

# Watch the logs to see output
kubectl logs -f test

# Find the PRIMARY, then destroy it
kubectl exec -it mongodb-in-k8s-1 -- /var/lib/mongodb-mms-automation/mongodb-linux-x86_64-4.0.10/bin/mongo
>rs.status()

kubectl delete pod mongodb-in-k8s-X

#Watch the output of the test pod - it will continue to be able to write data!

#Build the container
docker build -t jmimick/test .
