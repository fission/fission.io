all: fission-all-nodeport.yaml fission-all-loadbalancer.yaml

fission-all-nodeport.yaml: fission.yaml fission-nodeport.yaml
	cat fission.yaml fission-nodeport.yaml > fission-all-nodeport.yaml

fission-all-loadbalancer.yaml: fission.yaml fission-cloud.yaml
	cat fission.yaml fission-cloud.yaml > fission-all-loadbalancer.yaml
