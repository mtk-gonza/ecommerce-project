# E-commerce API

API REST desarrollada con **FastAPI**, conectada a una base de datos **MySql**, utilizando:
**SQLAlchemy** como ORM.
**Alembic** para migraciones.  
**Pydantic** para validaciones.

## ⚙️ Requisitos
- Python 3.12+
- FastAPI
- SQLAlchemy
- MySql
- pipenv o virtualenv (recomendado)
- Alembic

## 📦 Instalación y ▶️ Ejecución del servidor

Recordar copiar, completar y renombrar el .env.example a .env dentro de /ecom-backend
```bash

- Clonar el repositorio:
 git clone https://github.com/mtk-gonza/ecommerce-project.git
 cd ecom-backend

- Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

- Instalar dependencias
pip install -r requirements.txt

- Ejecución del servidor
uvicorn app.main:app --reload --port 3050

ENV=dev uvicorn app.main:app --reload
ENV=prod uvicorn app.main:app --host 0.0.0.0 --port 8000

- Swagger UI
http://127.0.0.1:8000/docs

```
