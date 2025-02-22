#!/bin/bash

curl -sfL https://get.rke2.io | sh -
mkdir -p /etc/rancher/rke2/
cat <<EOF> /etc/rancher/rke2/config.yaml
token: ${2:-rke2rancherlab}
etcd-snapshot-schedule-cron: "0 */1 * * *"
tls-san:
  - ${1:-rancher.student.lab}
EOF

systemctl enable --now rke2-server

curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

mkdir -p ~/.kube/

cp /etc/rancher/rke2/rke2.yaml ~/.kube/config
cp /var/lib/rancher/rke2/bin/kube* /usr/local/bin/.

/usr/local/bin/helm repo add jetstack https://charts.jetstack.io
/usr/local/bin/helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
/usr/local/bin/helm repo update

/usr/local/bin/helm upgrade --install cert-manager jetstack/cert-manager  \
--namespace cert-manager \
--create-namespace \
--set crds.enabled=true \
--wait

echo -e "\n\nAguarde 2 minutos para instalar o Rancher"
sleep 90

/usr/local/bin/helm install rancher rancher-latest/rancher \
--namespace cattle-system \
--create-namespace \
--set hostname=${1:-rancher.student.lab} \
--set bootstrapPassword=${2:-rke2rancherlab} \
--set replicas=1 \
--wait

echo -en "\n\n[Bootstrap Password]: "

/usr/local/bin/kubectl get secret --namespace cattle-system bootstrap-secret -o go-template='{{.data.bootstrapPassword|base64decode}}{{ "\n" }}'
