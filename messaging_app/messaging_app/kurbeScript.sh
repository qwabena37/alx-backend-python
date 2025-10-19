#!/bin/bash

# Check if Minikube is installed
if ! command -v minikube &> /dev/null
then
    echo "Minikube could not be found. Please install Minikube first."
    exit 1
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null
then
    echo "kubectl could not be found. Please install kubectl first."
    exit 1
fi

# Start a Minikube cluster
echo "Starting Kubernetes cluster using Minikube..."
minikube start --driver=docker

# Verify the cluster is running
echo "Verifying the cluster status..."
kubectl cluster-info

# Get the list of available pods
echo "Retrieving available pods..."
kubectl get pods
