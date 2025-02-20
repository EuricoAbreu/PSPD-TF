# Configuração do Cluster K3S

Este documento descreve o processo feito pelo grupo para instalar e configurar o **K3S** para a criação de um cluster Kubernetes leve e eficiente.

---

## 1. Configuração do Nó Mestre

No servidor principal (nó mestre), foi instalado o **K3S** executando:

```sh
curl -sfL https://get.k3s.io | sh -
```

Isso iniciou o **K3S** e criou um cluster Kubernetes de nó único.

Para verificar o status do cluster:

```sh
kubectl get nodes
```

Em seguida, foi obtido o **token** necessário para adicionar novos nós ao cluster:

```sh
sudo cat /var/lib/rancher/k3s/server/node-token
```

Também foi obtido o **IP do nó mestre** para que os nós secundários pudessem se conectar:

```sh
ip a
```

---

## 2. Adição de Nós ao Cluster

Nos nós que foram adicionados ao cluster, foi executado:

```sh
curl -sfL https://get.k3s.io | K3S_URL="https://<IP-DO-MESTRE>:6443" K3S_TOKEN="<TOKEN>" sh -
```

- `<IP-DO-MESTRE>` foi substituído pelo IP do nó mestre.
- `<TOKEN>` foi substituído pelo valor obtido anteriormente.

Para verificar se os nós foram adicionados corretamente, foi executado no **nó mestre**:

```sh
kubectl get nodes
```

Com isso, os nós apareceram na lista, confirmando que o cluster estava configurado corretamente.

---

## 3. Gerenciamento do K3S

Caso fosse necessário reiniciar o serviço do **K3S**, foi utilizado:

```sh
sudo systemctl restart k3s
```

Para remover **K3S** de um nó, foi utilizado:

```sh
sudo k3s-uninstall.sh
```

---

## 4. Conclusão

Com esses passos, o grupo configurou e testou o cluster **K3S** com sucesso.
