from decimal import Decimal
from app.domain.entities.coupon import Coupon
from app.domain.ports.coupon_repository import CouponRepositoryPort
from app.domain.exceptions import EntityNotFoundException, BusinessRuleException

class CouponService:
    def __init__(self, coupon_repository: CouponRepositoryPort):
        self.coupon_repository = coupon_repository

    def create_coupon(self, coupon_data: dict) -> Coupon:
        coupon = Coupon(**coupon_data)
        return self.coupon_repository.save(coupon)

    def get_coupon(self, coupon_id: int) -> Coupon:
        coupon = self.coupon_repository.find_by_id(coupon_id)
        if not coupon:
            raise EntityNotFoundException(f"Cupón {coupon_id} no encontrado")
        return coupon

    def validate_coupon(self, code: str, order_amount: Decimal) -> Coupon:
        coupon = self.coupon_repository.find_by_code(code)
        if not coupon:
            raise EntityNotFoundException(f"Cupón {code} no encontrado")
        if not coupon.is_valid(order_amount):
            raise BusinessRuleException("Cupón no válido para esta orden")
        return coupon

    def apply_coupon(self, code: str, order_amount: Decimal) -> Decimal:
        coupon = self.validate_coupon(code, order_amount)
        coupon.use()
        self.coupon_repository.save(coupon)
        return coupon.calculate_discount(order_amount)