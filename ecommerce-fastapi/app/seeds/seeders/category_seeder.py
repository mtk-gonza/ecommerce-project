from sqlalchemy.orm import Session
from app.infrastructure.db.models.category_model import CategoryModel
from app.seeds.data.categories_data import CATEGORIES

def category_seeder(session: Session):
    existing_categories = session.query(CategoryModel).count()
    if existing_categories > 0:    
        print(f'⚠️  Ya existen {existing_categories} categorias, se omite la inserción.')
        return
    
    for category_data in CATEGORIES:
        category = CategoryModel(**category_data)
        session.add(category)
        session.flush() 

    session.commit()
    print(f'{len(CATEGORIES)} CATEGORIES inserted correctly.')