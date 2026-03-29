from sqlalchemy.orm import Session
from app.infrastructure.db.models.role_model import RoleModel
from app.seeds.data.roles_data import ROLES

def role_seeder(session: Session):
    existing_roles = session.query(RoleModel).count()
    if existing_roles > 0:
        print(f'⚠️  Ya existen {existing_roles} roles, se omite la inserción.')
        return

    for role_data in ROLES:
        role = RoleModel(**role_data)
        session.add(role)
        session.flush()
    session.commit()
    print(f'{len(ROLES)} ROLES inserted correctly.')