from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.interfaces.api.v1.schemas.product_schema import ProductCreateSchema, ProductUpdateSchema, ProductSchema
from app.application.services.product_service import ProductService
from app.interfaces.api.v1.dependencies.services import get_product_service
from app.interfaces.api.v1.dependencies.auth import get_current_user, get_current_admin_user
from app.domain.entities.user import User
from app.domain.exceptions import EntityNotFoundException, ValidationError

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreateSchema, product_service: ProductService = Depends(get_product_service), current_user: User = Depends(get_current_admin_user)):
    try:
        product = product_service.create_product(product_data.model_dump())
        return product
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=List[ProductSchema])
def list_products(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), category_id: Optional[int] = None, product_service: ProductService = Depends(get_product_service)):
    return product_service.list_products(skip=skip, limit=limit, category_id=category_id)

@router.get("/search", response_model=List[ProductSchema])
def search_products(q: str = Query(..., min_length=2), skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), product_service: ProductService = Depends(get_product_service)):
    return product_service.search_products(query=q, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, product_service: ProductService = Depends(get_product_service)):
    try:
        return product_service.get_product(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/slug/{slug}", response_model=ProductSchema)
def get_product_by_slug(slug: str, product_service: ProductService = Depends(get_product_service)):
    try:
        return product_service.get_product_by_slug(slug)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product_data: ProductUpdateSchema, product_service: ProductService = Depends(get_product_service), current_user: User = Depends(get_current_admin_user)):
    try:
        return product_service.update_product(product_id, product_data.model_dump(exclude_unset=True))
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, product_service: ProductService = Depends(get_product_service), current_user: User = Depends(get_current_admin_user)):
    try:
        product_service.delete_product(product_id)
    except EntityNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))