# Recomendador de Autores y Libros

## Descripción

Este proyecto es una aplicación de Streamlit que recomienda textos basados en un autor y título ingresados por el usuario. Utiliza técnicas de procesamiento de lenguaje natural y algoritmos de similitud de coseno para generar recomendaciones relevantes. *(Sistema de recomendaciones basado en contenidos).*

## Instalación

### 1. Clona este repositorio.
### 2. Crea un entorno virtual.

### 2.1. Crear entorno virtual en Windows
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

### 2.2. Crear entorno virtual en macOS

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

### 3. Descargar archivo `requirements.txt`

```bash
pip install -r requirements.txt
```

### Corre el código ejecutando la linea
```bash
streamlit run app.py
```






