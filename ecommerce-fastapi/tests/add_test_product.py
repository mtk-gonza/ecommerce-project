import os
import sys
from decimal import Decimal
from datetime import datetime

# Agregar el proyecto al path para importar módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.infrastructure.db.session import engine, SessionLocal
from app.infrastructure.db.models.product_model import ProductModel
from app.domain.enums import ProductStatus, Currency

def add_test_product():
    """Agrega un producto de prueba a la BD"""
    db = SessionLocal()
    
    try:
        # Verificar si ya existe
        existing = db.query(ProductModel).filter(ProductModel.sku == "TEST-001").first()
        if existing:
            print(f"✅ Producto TEST-001 ya existe con ID: {existing.id}")
            return existing.id
        
        # Crear nuevo producto
        product = ProductModel(
            sku="TEST-002",
            slug="producto-prueba 2",
            name="Producto de Prueba 2",
            description="Producto creado para testing de órdenes y pagos",
            base_price=99.99,
            currency=Currency.USD,
            cost_price=50.00,
            stock=100,
            low_stock_threshold=10,
            status=ProductStatus.ACTIVE,
            is_visible=True,
            is_featured=False,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.add(product)
        db.commit()
        db.refresh(product)
        
        print(f"✅ Producto creado exitosamente con ID: {product.id}")
        return product.id
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    product_id = add_test_product()
    print(f"\n🎯 Usa product_id={product_id} para crear órdenes de prueba")