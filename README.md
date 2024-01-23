# 5-Data-Quality


1. [Instalar y ejecutar airflow](#schema1)
2. 


<hr>
<a name='schema1'></a>

## 1. Instalar y ejecutar airflow

- Crear un directorio para el proyecto
- Ir a [Running Airflow in Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html)
  - Navegar hasta el punto `Fetching docker-compose.yaml` y ejecutar en un terminal.
  ```
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.0/docker-compose.yaml'
  ```
  Y nos crea el archivo `docker-compose.yaml`
- Crear las carpetas necesarias para la ejecuación de Airflow
```
mkdir -p ./dags ./logs ./plugins ./config
```
-  Crear un archivo de entrono
```
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
- Parar el resto te contenedores 
```
docker stop nombre-contenedor
```
- Borrar los contenedores
```
docker rm nombre_contenedor
```
- Eliminar los servicios correspondientes
```
docker-compose -f tu_archivo_docker_compose.yml down
```
- Volver a ejecutar solo el conjunto que quieres ejecutar, en este caso 5-data-quality

```
docker-compose -f tu_archivo_docker_compose.yml up -d
```
- Ejecutar airflow
```
docker-compose up -d
```

- Inicializar la base de datos
```
docker-compose up airflow-init
```
- Si da error, es porque hay que modificar el archivo `docker-compose.yaml`
- Ejecutar airflow
```
docker-compose up -d
```
- Vamos al localhost http://localhost:8080/home

Tanto para el usuario y contraseña poner, airflow

- Crear las conecciones a AWS en airflow
  - aws_credentials
  - redshift
