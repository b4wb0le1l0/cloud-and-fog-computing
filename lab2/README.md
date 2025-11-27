# Системный монитор

### [Основная документация](https://github.com/b4wb0le1l0/cloud-and-fog-computing/blob/main/lab1/README.md)

## Запуск приложения (lab2)

```bash
cd lab1

minikube start
kubectl get nodes

# Сборка образа
minikube image build -t lab1-front:v2 -f Dockerfile .

cd ../lab2

kubectl apply -f deploy-redis.yaml
kubectl apply -f service-redis.yaml
kubectl apply -f deploy-front.yaml
kubectl apply -f service-front.yaml

# или

kubectl apply -f .

# Проверка
kubectl get all
minikube service front-service
```

Остановка
```bash
minikube stop
```

