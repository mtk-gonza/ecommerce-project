from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings
from app.infrastructure.db.base import Base

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# 🔥 FALTA ESTO
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🛠 Función para crear las tablas
def init_db():
    # Importar los modelos aquí para que se registren en Base.metadata antes de crear tablas
    from app.infrastructure.db.models import (
        cart_model,
        category_model,
        marketing_model,
        order_model,
        payment_model,
        product_model,
        user_model
    )
    Base.metadata.create_all(bind=engine)
    print("Tablas registradas:")
    for table in Base.metadata.sorted_tables:
        print(f"  - {table.name}")