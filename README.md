# Recomendador de Autores y Libros

## Descripción

Este proyecto es una aplicación de Streamlit que recomienda textos basados en un autor y título ingresados por el usuario. Utiliza técnicas de procesamiento de lenguaje natural y algoritmos de similitud de coseno para generar recomendaciones relevantes. *(Sistema de recomendaciones basado en contenidos).*

## Instalación

### 1. Clona este repositorio.
### 2. Crea un entorno virtual.

### 2.1. Crear entorno virtual en macOS

```bash
python3 -m venv nombre_del_entorno
```
#### Activar entorno virtual
```bash
source nombre_del_entorno/bin/activate
```
#### Desactivar entorno virtual
```bash
deactivate
```

### 2.2. Crear entorno virtual en Windows
#### Dar permisos para el entorno virtual
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
#### Crear el entorno virtual
```bash
python -m venv nombre_del_entorno
```
#### Activar entorno virtual
```bash
.\nombre_del_entorno\Scripts\Activate
```
#### Desactivar entorno virtual
```bash
deactivate
```

### 3. Descargar archivo `requirements.txt`

```bash
pip install -r requirements.txt
```

### 4. Descargar la data de origen de los libros

#### Abre tu terminal y ejecuta el siguiente comando:
```bash
git clone --filter=blob:none --no-checkout https://github.com/karen-pal/borges.git
```
Esto clona el repositorio sin descargar todos los archivos, sino solo los neecsarios.

#### Navega a la carpeta clonada:
```bash
cd borges
```

### Configura sparse-checkout:
```bash
git sparse-checkout init --cone
```

### Agrega la carpeta específica que deseas clonar:
```bash
git sparse-checkout set datasets/datasets_pkl
```

### Finalmente, descarga la carpeta:
```bash
git checkout
```

### Cambia la ruta de tus archivos:
```Ve a la linea 12 del codigo app.py y cambia la ruta donde está tu carpeta "datasets_pkl"```

### Corre el código ejecutando la linea
```bash
streamlit run app.py
```






