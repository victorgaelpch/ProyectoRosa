# Proyecto Rosa - Café sin filas ☕

Bienvenido al sistema de pedidos en línea para Café sin filas.

## Requisitos

- Python 3.10 o superior
- PostgreSQL (si usas base de datos remota)
- Git (opcional, para clonar el repositorio)

2. **Crea el entorno virtual**

   ```sh
   python -m venv venv
   ```

3. **Activa el entorno virtual**

   En Windows:
   ```sh
   venv\Scripts\activate
   ```

   En Mac/Linux:
   ```sh
   source venv/bin/activate
   ```

4. **Instala las dependencias**

   ```sh
   pip install -r requirements.txt
   ```

5. **Configura la base de datos**

   Edita el archivo `proyect/SisWebCafe/settings.py` con los datos de tu base PostgreSQL.

6. **Aplica las migraciones(si no se han hecho)**

   ```sh
   python manage.py migrate
   ```

7. **Crea un superusuario(si no se ha hecho)**

   ```sh
   python manage.py createsuperuser
   ```

8. **Ejecuta el servidor**

   ```sh
   python manage.py runserver
   ```

## Uso

- Accede a la app en [http://localhost:8000](http://localhost:8000)
