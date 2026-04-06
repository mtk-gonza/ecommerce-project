ecommerce-fastapi/
├── 📁app/
│   ├── 📁application/
│   │   └── 📁services/
│   │       ├── auth_service.py
│   │       ├── cart_service.py
│   │       ├── category_service.py
│   │       ├── coupon_service.py
│   │       ├── order_service.py
│   │       ├── payment_service.py
│   │       ├── product_service.py
│   │       ├── review_service.py
│   │       └── user_service.py
│   │
│   ├── 📁config/
│   │   └── settings.py
│   │
│   ├── 📁domain/
│   │   ├── 📁entities/
│   │   │   ├── cart.py
│   │   │   ├── category.py
│   │   │   ├── coupon.py
│   │   │   ├── order.py
│   │   │   ├── payment.py
│   │   │   ├── product.py
│   │   │   ├── review.py
│   │   │   └── user.py
│   │   ├── 📁ports/
│   │   │   ├── cart_repository.py
│   │   │   ├── category_repository.py
│   │   │   ├── coupon_repository.py
│   │   │   ├── order_repository.py
│   │   │   ├── payment_repository.py
│   │   │   ├── product_repository.py
│   │   │   ├── review_repository.py
│   │   │   └── user_repository.py
│   │   ├── enums.py
│   │   └── exceptions.py
│   │
│   ├── 📁infrastructure/
│   │   ├── 📁db/
│   │   │   ├── base.py
│   │   │   ├── session.py
│   │   │   └── 📁models/
│   │   │       ├── base_model.py
│   │   │       ├── marketing_model.py
│   │   │       ├── order_model.py
│   │   │       ├── payment_model.py
│   │   │       ├── product_model.py
│   │   │       └── user_model.py
│   │   ├── 📁external/
│   │   │   └── mercadopago_client.py 
│   │   ├── 📁logging/
│   │   │   ├── config.py
│   │   │   ├── formatter.py
│   │   │   ├── handlers.py
│   │   │   └── logger.py
│   │   ├── 📁mappers/
│   │   │   ├── cart_mapper.py
│   │   │   ├── category_mapper.py
│   │   │   ├── order_mapper.py
│   │   │   ├── payment_mapper.py
│   │   │   ├── product_mapper.py
│   │   │   └── user_mapper.py
│   │   ├── 📁repositories/
│   │   │   ├── cart_repository_impl.py
│   │   │   ├── category_repository_impl.py
│   │   │   ├── order_repository_impl.py
│   │   │   ├── payment_repository_impl.py
│   │   │   ├── product_repository_impl.py
│   │   │   └── user_repository_impl.py
│   │   ├── 📁security/
│   │   │   ├── jwt_handler.py
│   │   │   ├── password_handler.py
│   │   │   └── role_handler.py
│   │   └── 📁storage/
│   │       └── file_storage.py
│   │
│   ├── 📁interfaces/
│   │   └── 📁api/
│   │       └── 📁v1/
│   │           ├── 📁dependencies/
│   │           │   ├── auth.py
│   │           │   ├── db.py
│   │           │   ├── repositories.py
│   │           │   ├── role.py
│   │           │   └── services.py
│   │           ├── 📁routes/
│   │           │   ├── auth_router.py
│   │           │   ├── cart_router.py
│   │           │   ├── category_router.py
│   │           │   ├── order_router.py
│   │           │   ├── payment_router.py
│   │           │   ├── product_router.py
│   │           │   └── user_router.py
│   │           ├── 📁schemas/
│   │           │   ├── auth_schema.py
│   │           │   ├── cart_schema.py
│   │           │   ├── order_schema.py
│   │           │   ├── payment_schema.py
│   │           │   ├── product_schema.py
│   │           │   └── user_schema.py
│   │           └── handlers.py
│   │
│   ├── 📁logs/
│   │
│   ├── 📁seeds/
│   │
│   ├── 📁utils/
│   │   ├── jwt_handler.py
│   │   ├── password_utils.py
│   │   ├── role_handler.py
│   │   └── slug_handler.py
│   │
│   └── main.py
│
├── .env                           
├── .env.example
├── alembic.ini
├── Dockerfile
├── README.md
├── requirements-devs.txt
├── requirements.txt
└── STRUCTURE.md