# Hound Express | API de guías

API REST en Django para la paquetería Hound Express. Guarda las guías de envío y el historial de cambios de estado. La usa el frontend [Hound-Express-Modulo-30](https://github.com/Moremaster123/Hound-Express-Modulo-30).

## Tecnologías

- Python y Django 6.1
- Django REST Framework
- django-cors-headers (permite las peticiones del frontend)
- SQLite

## Modelos

| Modelo | Campos |
|---|---|
| `Guia` | trackingNumber (único), recipient, origin, destination, createdAt, currentStatus |
| `Estatus` | guideId (llave foránea a Guia), status, updatedBy |
| `Usuario` | name, email, password, createdAt |

Los estados posibles de una guía son Pendiente, En tránsito y Entregada.

## Cómo ejecutarlo

```bash
python -m venv venv
venv\Scripts\activate        # en Linux o macOS: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La API queda en `http://127.0.0.1:8000/api/`.

## Endpoints

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/guias/` | Lista todas las guías con su historial |
| POST | `/api/crear-guia/` | Crea una guía |
| GET | `/api/obtener-guia/<id>/` | Muestra una guía |
| PUT, PATCH | `/api/actualizar-guia/<id>/` | Actualiza una guía o solo su estado |
| DELETE | `/api/eliminar-guia/<id>/` | Elimina una guía |

Ejemplo para crear una guía:

```bash
curl -X POST http://127.0.0.1:8000/api/crear-guia/ -H "Content-Type: application/json" -d "{\"trackingNumber\": \"HE-0001\", \"recipient\": \"Ana Lopez\", \"origin\": \"Puebla\", \"destination\": \"Monterrey\"}"
```

## Autor

Juan Carlos González Herrera · [LinkedIn](https://www.linkedin.com/in/juan-carlos-desarrollador-web) · [Portafolio](https://moremaster123.github.io)
