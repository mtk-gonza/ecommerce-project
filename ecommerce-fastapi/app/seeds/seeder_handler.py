from app.infrastructure.db.session import SessionLocal, init_db
from .seeders.category_seeder import category_seeder
from .seeders.license_seeder import license_seeder
from .seeders.role_seeder import role_seeder
from .seeders.product_seeder import product_seeder
from .seeders.user_seeder import user_seeder

def run_seeder():
    init_db()
    db = SessionLocal()
    try:
        print('Starting the seeding process...')

        category_seeder(db)
        license_seeder(db)
        role_seeder(db)
        product_seeder(db)
        user_seeder(db)   
             
        print('✅ Seeding successfully completed.')
    except Exception as e:
        print(f'❌ Error during sowing: {e}')
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seeder()