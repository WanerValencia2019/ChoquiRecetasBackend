# ChoquiRecetasBackend
API de recetas


### Instalación

1. **Paso 1 - Creación del entorno virtual**
      - `python -m venv env`
      
2. **Paso 2 - Instalación de dependencias**
      - `pip install -r requirements.txt`
      
3. **Paso 3 - Migración inicial**
      - `python manage.py migrate`
      
4. **Paso 4- Migrar modelos**
      - `python manage.py makemigrations`
      - `python manage.py migrate`
5. **Paso 5- Crear usuario inicial**
   - #### Create super user
      - ``python manage.py createsuperuser``   
   - #### Run server
     - ``python manage.py runserver 127.0.0.1:8000``
     
## Configuración
  - #### Crear un archivo con el nombre ``.env``
    - El archivo debe contener las siguientes propiedades: ***Ejemplo***
      - SECRET_KEY= &e_#wg+qa_7tx_9m)09rs$%6&kw38umd&q0xni9*5lb*rbg62l
      - EMAIL_HOST_USER = correo@gmail.com
      - EMAIL_HOST_PASSWORD = contraseña
      - SOCIAL_AUTH_FACEBOOK_KEY=80708432326600631
      - SOCIAL_AUTH_FACEBOOK_SECRET=cd141ea5c62737hd723c246dce420b7e1113427
