## Environment

- Kubernetes Cluster v1.18 on Alicloud
- kubectl v1.22.3

## Basic Info

content

```
├── config-map.yml      # config map for nginx config
├── deployment-api.yml  # deployment for API service
├── deployment-db.yml   # deployment for database
├── hpa-api.yml         # HPA for api service
├── ingress.yml         # Ingress for API
├── pvc-db.yml          # PV & PVC for database storage
├── secret.yml          # docker & database credential
├── service-api.yml     # service for API
└── service-db.yml      # service for database
```

Web API service is demonstrating with nginx:alpine container.

## Quick Start

Create a separated namespace for test

```
$ kubectl create ns wc-test
```

Make sure configMaps, secrets and PVC are created first.

```
$ kubectl -n wc-test apply -f config-map.yml
$ kubectl -n wc-test apply -f secrets.yml
$ kubectl -n wc-test apply -f pvc-db.yml
```

Then create other resources.

```
$ kubectl -n wc-test apply -f deployment-db.yml
$ kubectl -n wc-test apply -f deployment-api.yml
$ kubectl -n wc-test apply -f hpa-api.yml
$ kubectl -n wc-test apply -f service-api.yml
$ kubectl -n wc-test apply -f service-db.yml
$ kubectl -n wc-test apply -f ingress.yml
```

Don't forget to delete these resources after test.

```
$ for i in *.yml; do kubectl -n wc-test delete -f $i; done

# delete namespace at last
$ kubectl delete ns wc-test
```
