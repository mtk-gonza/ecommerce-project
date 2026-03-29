from app.domain.enums.image_type import ImageType
from app.utils.slug_handler import generate_slug

LICENSES = [
    {
        'name':'Pokemon', 
        'description':'Atrapa todos los que puedas y disfruta de una colección llena de amigos.',
        'slug': generate_slug('Pokemon'),
        'images': [
            {
                'path': 'images/pokemon/license/pokemon_logo.webp',
                'image_type': ImageType.LOGO.value.lower(),
                'is_primary': True
            }
        ] 
    },
    {
        'name':'Star Wars', 
        'description':'Disfruta de una saga que sigue agregando personajes a su colección.', 
        'slug': generate_slug('Star Wars'),
        'images': [
            {
                'path': 'images/star-wars/license/star-wars_logo.webp',
                'image_type': ImageType.LOGO.value.lower(),
                'is_primary': True
            }
        ] 
    },
    {        
        'name':'Harry Potter', 
        'description':'Revive los recuerdos de una saga llena de magia y encanto.',
        'slug': generate_slug('HarryPotter'), 
        'images': [
            {
                'path': 'images/harry-potter/licence/harry-potter_logo.webp',
                'image_type': ImageType.LOGO.value.lower(),
                'is_primary': True
            }
        ] 
    },
    {
        'name':'Naruto', 
        'description':'Disfruta de la historia de un ninja adolescente',
        'slug': generate_slug('Naruto'),
        'images': [
            {
                'path': 'images/Naruto/license/naruto_logo.webp',
                'image_type': ImageType.LOGO.value.lower(),
                'is_primary': True
            }
        ] 
    },
    {
        'name':'Dragon Ball', 
        'description':'Disfruta de la historia de un guerrero saiyajin', 
        'slug': generate_slug('Dragon Ball'),
        'images': [
            {
                'path': 'images/dragon-ball/license/dragon-ball_logo.webp',
                'image_type': ImageType.LOGO.lower(),
                'is_primary': True
            }
        ] 
    }
]