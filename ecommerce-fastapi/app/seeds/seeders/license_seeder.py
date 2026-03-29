from sqlalchemy.orm import Session
from app.infrastructure.db.models.license_model import LicenseModel
from app.infrastructure.db.models.image_model import ImageModel
from app.domain.enums.entity_type import EntityType
from app.seeds.data.licenses_data import LICENSES

def license_seeder(session: Session):    
    existing_licenses = session.query(LicenseModel).count()
    if existing_licenses > 0:
        print(f'⚠️{existing_licenses} licenses already exist, insertion is omitted.')
        return
    
    for license_data in LICENSES:
        images_data = license_data.pop('images', [])
        licence = LicenseModel(**license_data)
        session.add(licence)
        session.flush()

        for img_data in images_data:
            image = ImageModel(
                path=img_data['path'],
                entity_type=EntityType.LICENSE.value,
                entity_id=licence.id,
                image_type=img_data.get('image_type'),
                is_primary=img_data.get('is_primary', False)
            )
            session.add(image)     

    session.commit()
    print(f'{len(LICENSES)} LICENCES inserted correctly.')