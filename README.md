# api-go-nats
 Api go nats

## Construir Imagen

Entrar a la carpeta del servicio que se quiere publicar y ejecutar
```
sudo sh build.sh
```
## push imagen a docker

```
sudo docker push wildering/python-nats
```
## Publicar en Kubernetes
Publicamos la imagen en nuestro namespace proyecto [-n proyecto]
```
kubectl create deployment miapp-python-n --image=wildering/python-nats -n proyecto
```
## Crear servicio

```
kubectl expose deployment miapp-python-n --name=miapp-python-nats-srv --port=8080 --target-port=8080 -n proyecto
```

## Crear el Ingress ya sea para nginx o para Contour

Una vez creado lo ejecutamos
```
kubectl create -f ingress-gateway-countour.yaml
```
## Crear un registro DNS en google cloud

Se crea el registro DNS, que esta en nuestro archivo .yaml, el cual apuntará  a la ip
del ingresses ya sea de countour (envoy) o de nginx (nginx-ingress-controller)

## Desarrollo y depuración de servicios a nivel local
Las aplicaciones de Kubernetes suelen constar de varios servicios independientes, cada uno de los que se ejecutan en su propio contenedor. Desarrollar y depurar estos servicios en un clúster de Kubernetes remoto puede ser engorroso, lo que requiere que obtenga un shell en un contenedor en ejecución y ejecute las herramientas dentro del shell remoto.

```
telepresence --swap-deployment miapp-python-n --namespace proyecto
```

https://kubernetes.io/docs/tasks/debug-application-cluster/local-debugging/

## Instalar MongoDB en Ubuntu 18.04 (Google Cloud)
https://www.digitalocean.com/community/tutorials/como-instalar-mongodb-en-ubuntu-18-04-es


## Instalar Redis en Ubuntu 18.04 (Google Cloud)

https://cloud.google.com/community/tutorials/setting-up-redis
