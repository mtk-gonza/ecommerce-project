from sqlalchemy.orm import Session
from app.infrastructure.db.models.user_model import UserModel
from app.infrastructure.db.models.role_model import RoleModel
from app.infrastructure.db.models.user_roles_model import UserRolesModel
from app.seeds.data.users_data import USERS
from app.infrastructure.security.password_handler import hash_password

def user_seeder(session: Session):
    existing_users = session.query(UserModel).count()
    if existing_users > 0:
        print(f'⚠️  Ya existen {existing_users} usuarios, se omite la inserción.')
        return

    roles = session.query(RoleModel).all()
    roles_by_name = {role.name: role for role in roles}

    for user_data in USERS:
        role_names = user_data.get('roles', [])

        password_hashed = hash_password(user_data['password'])

        db_user = UserModel(
            email=user_data['email'],
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            password_hash=password_hashed,
            is_active=user_data.get('is_active', True),
            is_verified=user_data.get('is_verified', True)
        )

        session.add(db_user)
        session.flush()

        for role_name in role_names:
            role = roles_by_name.get(role_name)

            if not role:
                print(f'❌ Role "{role_name}" no encontrado para usuario "{user_data["username"]}".')
                continue

            session.add(UserRolesModel(
                user_id=db_user.id,
                role_id=role.id
            ))

    session.commit()
    print(f'✅ {len(USERS)} USUARIOS insertados correctamente con sus roles.')