# Configuração do Kubernetes Dashboard

Este documento descreve o processo realizado pelo grupo para instalar e configurar o **Kubernetes Dashboard**.

## 1. Instalação do Kubernetes Dashboard

O primeiro passo foi aplicar a configuração oficial do **Kubernetes Dashboard**:

```sh
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

## 2. Iniciando o Proxy do Kubernetes

Após a instalação, iniciamos o proxy para permitir o acesso ao painel:

```sh
kubectl proxy
```

## 3. Acessando o Dashboard

Com o proxy em execução, acessamos a interface web através do seguinte link:

```
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/
```

## 4. Criando o Admin User

Antes de gerar o token de acesso, criamos a conta de serviço do usuário administrador:

```sh
kubectl create serviceaccount admin-user -n kubernetes-dashboard
```

## 5. Gerando o Token de Acesso

Para acessar o painel administrativo, geramos um token de autenticação:

```sh
kubectl -n kubernetes-dashboard create token admin-user
```

O token gerado foi utilizado na interface do Kubernetes Dashboard para obter acesso total ao cluster.

---

Com isso, o **Kubernetes Dashboard** foi configurado e está pronto para uso.
