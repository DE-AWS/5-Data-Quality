# 5-Data-Quality


1. [Instalar y ejecutar airflow](#schema1)
2. [Data Scheduling en Apache Airflow](#schema2)
3. [Data Partitioning en Apache Airflow](#schema3)


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
    - admin -> connections:
      - connection_id : aws_credentials
      - connection_type: Amazon Web Services
      - Aws Access Key Id: Access key id fom iam user
      - Aws Secret Access Key Id: Secret access key form iam user
    - SAVE
  - redshift
    - admin -> connections:
      - connection_id : redshift
      - connection_type: Amazon Redshift
      - Host: url del endpoint de amazon redshift serverless
      - Schema: dev
      - Login: IAM USER
      - Password: contraseña
      - Port: 5439
    - SAVE
- Crea las variables en Airflow:
  - admin -> variables
    - s3_bucket : value -> nombre del bucket
    - s3_prefix: value -> data_pipelines


<hr>
<a name='schema2'></a>

## 2. Data Scheduling en Apache Airflow


Se refiere a la planificación y programación de flujos de trabajo de procesamiento de datos en Apache Airflow.

- **DAGs (Directed Acyclic Graphs):**

Los flujos de trabajo se definen utilizando DAGs, que consisten en tareas y sus dependencias.

- **start_date y schedule_interval:**

`start_date`: Especifica la fecha de inicio del DAG.
`schedule_interval`: Determina la frecuencia con la que se ejecuta el DAG (por ejemplo, diariamente, mensualmente).

- **Cron-Like Expressions:**

`schedule_interval` utiliza expresiones similares a cron para definir la frecuencia de ejecución.

- **Execution Date:**

Cada ejecución del DAG tiene una "Execution Date" asociada, determinada por start_date y schedule_interval.


```python
@dag(
    start_date=pendulum.datetime(2018, 1, 1, 0, 0, 0, 0),
    end_date=pendulum.datetime(2018, 2, 1, 0, 0, 0, 0),
    schedule_interval='@monthly',
    max_active_runs=1    
)
```
`start_date`: Especifica la fecha y hora de inicio del DAG. En este caso, el DAG comenzará el 1 de enero de 2018 
a la medianoche.

`end_date`: Indica la fecha y hora de finalización del DAG. En este caso, el DAG finalizará el 1 de febrero de 2018 
a la medianoche.

`schedule_interval`: Define la frecuencia con la que se ejecutará el DAG. En este caso, está configurado para 
ejecutarse mensualmente (`'@monthly'`), lo que significa que el DAG se ejecutará una vez al mes.

`max_active_runs`: Limita el número máximo de instancias del DAG que pueden ejecutarse simultáneamente. En este caso, 
se ha establecido en 1, lo que significa que solo puede haber una ejecución activa del DAG al mismo tiempo.

<hr>
<a name='schema3'></a>

## 3. Data Partitioning en Apache Airflow

Se refiere a la división de grandes conjuntos de datos en particiones más pequeñas para procesamiento paralelo y eficiente.

- **Partitioned Tasks:**

Se pueden definir tareas que operan sobre particiones específicas de datos.

- **Dynamic Task Generation:**

Utilizando parámetros, es posible generar dinámicamente tareas para cada partición de datos.

- **Parallelism:**

Permite la ejecución paralela de tareas en diferentes particiones, mejorando el rendimiento del procesamiento.

- **Ejemplo de Uso:**

Útl al procesar grandes conjuntos de datos en paralelo, como particionar un conjunto de datos por fecha para procesar 
cada día de forma independiente.


<hr>
<a name='schema4'></a>

## 4. Data Quality Requirements
Se refiere a los criterios o estándares que se establecen para evaluar y garantizar la calidad de los datos 
en un contexto específico. La calidad de los datos es un aspecto crítico en cualquier entorno donde se manipulan 
y utilizan datos, ya que afecta directamente la confiabilidad y la eficacia de los procesos y decisiones basadas en 
esos datos.


Algunos aspectos clave de los requisitos de calidad de datos incluyen:

- Precisión: La exactitud de los datos en relación con la realidad que representan.

- Integridad: La coherencia y la completitud de los datos, asegurando que no haya información faltante o inconsistente.

- Consistencia: La uniformidad y la estandarización de los datos en todo el conjunto.

- Actualidad: La relevancia temporal de los datos, asegurando que estén actualizados y reflejen la situación actual.

- Confiabilidad: La confianza en la fuente de los datos y en los métodos utilizados para recopilar, procesar y 
almacenar la información.

- Relevancia: La pertinencia y la aplicabilidad de los datos para los propósitos previstos.

- Complejidad: La capacidad de los datos para abordar la complejidad de la realidad que representan, especialmente 
en entornos donde se requiere manejar datos heterogéneos o de diversas fuentes.

- Seguridad y Privacidad: Garantizar que los datos se manejen de manera segura y cumplan con las regulaciones y 
políticas de privacidad.

Establecer requisitos claros de calidad de datos es esencial para asegurar que la información utilizada en análisis, 
informes y toma de decisiones sea confiable y precisa. Esto implica la implementación de prácticas y procesos que 
monitoreen, mantengan y mejoren continuamente la calidad de los datos a lo largo del tiempo.