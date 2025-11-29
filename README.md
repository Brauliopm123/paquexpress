# paquexpress
Sistema de trazabilidad y gestión de entregas para Paquexpress.
# Paquexpress

Proyecto desarrollado en Flutter y FastAPI para la gestión de entregas y trazabilidad de paquetes.

# Estructura del Proyecto

* **`app_flutter/`**: Código fuente de la aplicación móvil.
* **`api_fastapi/`**: Código fuente del backend REST.
* **`bd.sql`**: Script de la base de datos MySQL.

# Requisitos Previos

Flutter SDK (Versión X.X.X)
Python 3.8+ y pip
MySQL

# Instalación y Uso

# 1. Base de Datos (MySQL)

1.  Crea la base de datos `paquexpress` en tu servidor MySQL.
2.  Ejecuta el contenido del archivo `bd.sql`.

# 2. Backend (FastAPI)

1.  Navega a la carpeta `APII/`.
2.  Instala las dependencias: `pip install -r requirements.txt` (lo crearemos después).
3.  Ejecuta el servidor: `uvicorn main:app --reload` (ajusta la configuración de la BD).

# 3. Aplicación Móvil (Flutter)

1.  Navega a la carpeta `evaluacion3`.
2.  Instala las dependencias: `flutter pub get`.
3.  Ajusta la URL de la API en el código fuente (`lib/config.dart`).
4.  Ejecuta en un dispositivo o emulador: `flutter run`.

---

# Paso 2: Crear la Aplicación Flutter

Ahora crearemos la aplicación móvil dentro de la carpeta `evaluacion3`.

# 2.1 Crear la Aplicación

1.  Asegúrate de estar en la carpeta principal del repositorio (`EVALUACIONU3`).
2.  Ejecuta el comando de creación de Flutter, especificando la carpeta de destino:
    ```bash
    flutter create evaluacion3
    ```
    Esto creará toda la estructura de una aplicación Flutter dentro de la carpeta `evaluacion3/`.

# 2.2 Agregar Dependencias Necesarias

La aplicación requerirá varias librerías para la funcionalidad (GPS, Cámara, HTTP, Mapas).

1.  Navega a la carpeta de la aplicación:
    ```bash
    cd evaluacion3
    ```
2.  Abre el archivo **`pubspec.yaml`** y agrega las siguientes dependencias bajo `dependencies:`:

    ```yaml
    dependencies:
      flutter:
        sdk: flutter
      # HTTP para conectarse a FastAPI
      dio: ^5.0.0
      # Geolocalización para el GPS
      geolocator: ^11.0.0
      # Captura de foto de evidencia
      image_picker: ^1.0.0
      # Para manejar el estado de la aplicación
      provider: ^6.0.0
      # Para almacenamiento seguro del Token JWT
      flutter_secure_storage: ^9.0.0
      # Para la visualización de mapas (opcional, considera google_maps_flutter)
      # google_maps_flutter: ^2.0.0
    ```
3.  Guarda el archivo y ejecuta para obtener las dependencias:
    ```bash
    flutter pub get
    ```