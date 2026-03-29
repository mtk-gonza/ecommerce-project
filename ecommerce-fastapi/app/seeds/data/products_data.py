from app.domain.enums.image_type import ImageType
from app.domain.enums import ProductStatus, Currency
from app.utils.slug_handler import generate_slug

PRODUCTS = [
    {
        'name': 'Baby Yoda Blueball',
        'slug': generate_slug('Baby Yoda Blueball'),
        'description': 'Figura coleccionable de Baby Yoda (Grogu) - The Mandalorian Saga, edición limitada.',
        'price': 1799.99,
        'currency': Currency.ARS,
        'cost_price': 1000.99,
        'stock': 8,
        'discount': 5.00,
        'sku': 'STW001001',
        'status': ProductStatus.ACTIVE.value,       
        'is_featured': False,
        'license_id': 2,
        'category_id': 1,
        'images': [
            {
                'path': '/images/star-wars/funkos/baby-yoda-blueball_front.webp',
                'image_type': ImageType.FRONT.value,  # ✅ Usar .value en lugar de .lower()
                'is_primary': True
            },
            {
                'path': '/images/star-wars/funkos/baby-yoda-blueball_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Luke Skywalker & Grogu',  # ✅ Corregido typo (Skylwalker → Skywalker)
        'slug': generate_slug('Luke Skywalker & Grogu'),
        'description': 'Figura coleccionable de Luke Skywalker & Grogu - The Mandalorian Saga.',
        'price': 399.99,
        'currency': Currency.USD,
        'stock': 8,
        'discount': 15.00,
        'sku': 'STW001003',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 2,
        'category_id': 1,
        'images': [
            {
                'path': '/images/star-wars/funkos/luke-skywalker-grogu_front.webp',  # ✅ Slug en path
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/star-wars/funkos/luke-skywalker-grogu_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Stormtrooper Lightsaber',
        'slug': generate_slug('Stormtrooper Lightsaber'),
        'description': 'Figura coleccionable de Stormtrooper Lightsaber - Star Wars Saga.',
        'price': 1799.99,
        'stock': 8,
        'discount': 20.00,
        'sku': 'STW001004',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 2,
        'category_id': 1,
        'images': [
            {
                'path': '/images/star-wars/funkos/stormtrooper-lightsaber_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/star-wars/funkos/stormtrooper-lightsaber_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Charmander Smiley',
        'slug': generate_slug('Charmander Smiley'),
        'description': 'Figura coleccionable de Charmander - Pokemon Saga.',
        'price': 1799.99,
        'stock': 8,
        'discount': 10.00,
        'sku': 'PKM001001',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 1,
        'category_id': 1,
        'images': [
            {
                'path': '/images/pokemon/funkos/charmander-smiley_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/pokemon/funkos/charmander-smiley_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Dragonite Hi',  # ✅ Quitar caracteres especiales del nombre
        'slug': generate_slug('Dragonite Hi'),
        'description': 'Figura coleccionable de Dragonite - Pokemon Saga.',
        'price': 1799.99,
        'stock': 8,
        'discount': 10.00,
        'sku': 'PKM001002',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 1,
        'category_id': 1,
        'images': [
            {
                'path': '/images/pokemon/funkos/dragonite-hi_front.webp',  # ✅ Sin caracteres especiales
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/pokemon/funkos/dragonite-hi_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Pidgeotto Flying',
        'slug': generate_slug('Pidgeotto Flying'),
        'description': 'Figura coleccionable de Pidgeotto - Pokemon Saga.',
        'price': 1799.99,
        'stock': 8,
        'discount': 30.00,
        'sku': 'PKM001003',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': True,
        'license_id': 1,
        'category_id': 1,
        'images': [
            {
                'path': '/images/pokemon/funkos/pidgeotto-flying_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/pokemon/funkos/pidgeotto-flying_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Pikachu Smiley',
        'slug': generate_slug('Pikachu Smiley'),
        'description': 'Figura coleccionable de Pikachu - Pokemon Saga.',
        'price': 1799.99,
        'stock': 8,
        'discount': 10.00,
        'sku': 'PKM001004',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 1,
        'category_id': 1,
        'images': [
            {
                'path': '/images/pokemon/funkos/pikachu-smiley_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/pokemon/funkos/pikachu-smiley_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Vulpix Fancy',
        'slug': generate_slug('Vulpix Fancy'),
        'description': 'Figura coleccionable de Vulpix - Pokemon Saga.',
        'price': 99.99,
        'stock': 8,
        'discount': 10.00,
        'sku': 'PKM001005',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 1,
        'category_id': 1,
        'images': [
            {
                'path': '/images/pokemon/funkos/vulpix-fancy_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/pokemon/funkos/vulpix-fancy_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Harry Potter & Hedwig',  # ✅ Corregido typo (Hegwid → Hedwig)
        'slug': generate_slug('Harry Potter & Hedwig'),
        'description': 'Figura coleccionable de Harry Potter & Hedwig - Harry Potter Saga.',
        'price': 1799.99,
        'stock': 11,
        'discount': 10.00,
        'sku': 'HPT001001',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 3,
        'category_id': 1,
        'images': [
            {
                'path': '/images/harry-potter/funkos/harry-potter-hedwig_front.webp',  # ✅ Path limpio
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/harry-potter/funkos/harry-potter-hedwig_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Kakashi Hatake Shippuden',
        'slug': generate_slug('Kakashi Hatake Shippuden'),
        'description': 'Kakashi Hatake Shippuden',
        'price': 1999.99,
        'stock': 20,
        'discount': 10.00,
        'sku': 'NRT001001',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': False,
        'license_id': 4,
        'category_id': 1,
        'images': [
            {
                'path': '/images/naruto/funkos/kakashi-hatake-shippuden_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/naruto/funkos/kakashi-hatake-shippuden_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Harry Potter T-Shirt',  # ✅ Nombre más descriptivo
        'slug': generate_slug('Harry Potter T-Shirt'),
        'description': 'Remera coleccionable de Harry Potter.',
        'price': 100.00,
        'stock': 999,
        'discount': 10.00,
        'sku': 'HPT003001',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': True,
        'license_id': 3,
        'category_id': 2,
        'images': [
            {
                'path': '/images/harry-potter/t-shirts/harry-potter_front.webp',
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/harry-potter/t-shirts/harry-potter_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    },
    {
        'name': 'Goku Kamehameha Keychain',
        'slug': generate_slug('Goku Kamehameha Keychain'),
        'description': 'Llavero coleccionable de Goku.',
        'price': 100.00,
        'stock': 999,
        'discount': 10.00,
        'sku': 'DBZ003001',
        'status': ProductStatus.ACTIVE.value,
        'is_featured': True,
        'license_id': 5,
        'category_id': 3,
        'images': [
            {
                'path': '/images/dragon-ball/keychains/goku-kamehameha_front.webp',  # ✅ Path limpio
                'image_type': ImageType.FRONT.value,
                'is_primary': True
            },
            {
                'path': '/images/dragon-ball/keychains/goku-kamehameha_back.webp',
                'image_type': ImageType.BACK.value,
                'is_primary': False
            }
        ]
    }
]