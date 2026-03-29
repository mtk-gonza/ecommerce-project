from typing import List
from app.domain.entities.review import Review
from app.domain.ports.review_repository import ReviewRepositoryPort
from app.domain.ports.product_repository import ProductRepositoryPort
from app.domain.exceptions import EntityNotFoundException, ValidationError

class ReviewService:
    def __init__(self, review_repository: ReviewRepositoryPort, product_repository: ProductRepositoryPort):
        self.review_repository = review_repository
        self.product_repository = product_repository

    def create_review(self, product_id: int, user_id: int, rating: int, title: str = None, comment: str = None) -> Review:
        product = self.product_repository.find_by_id(product_id)
        if not product:
            raise EntityNotFoundException(f"Producto {product_id} no encontrado")
        
        review = Review(
            id=None,
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            title=title,
            comment=comment
        )
        return self.review_repository.save(review)

    def approve_review(self, review_id: int) -> Review:
        review = self.review_repository.find_by_id(review_id)
        if not review:
            raise EntityNotFoundException(f"Reseña {review_id} no encontrada")
        review.approve()
        return self.review_repository.save(review)

    def get_product_reviews(self, product_id: int, approved_only: bool = True) -> List[Review]:
        return self.review_repository.find_by_product_id(product_id, approved_only=approved_only)