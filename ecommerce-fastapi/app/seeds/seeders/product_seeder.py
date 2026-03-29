from sqlalchemy.orm import Session
from app.infrastructure.db.models.product_model import ProductModel
from app.infrastructure.db.models.image_model import ImageModel
from app.seeds.data.products_data import PRODUCTS

def product_seeder(session: Session):
    existing_products = session.query(ProductModel).count()
    if existing_products > 0:
        print(f'⚠️  Ya existen {existing_products} productos, se omite la inserción.')
        return
    
    for product_data in PRODUCTS:
        images_data = product_data.pop('images', [])
        product = ProductModel(**product_data)
        session.add(product)
        session.flush()

        for img_data in images_data:
            image = ImageModel(
                path=img_data['path'],
                entity_type='product',  # ✅ Polimórfico
                entity_id=product.id,   # ✅ ID del producto recién creado
                image_type=img_data.get('image_type'),
                is_primary=img_data.get('is_primary', False)
            )
            session.add(image)
    
    session.commit()
    print(f'✅ {len(PRODUCTS)} PRODUCTOS insertados correctamente con sus imágenes.')