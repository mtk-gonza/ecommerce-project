class DomainException(Exception):
    """Excepción base del dominio"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ValidationError(DomainException):
    """Error de validación de entidad"""
    pass

class BusinessRuleException(DomainException):
    """Violación de regla de negocio"""
    pass

class InsufficientStockException(BusinessRuleException):
    """Stock insuficiente para operación"""
    pass

class InvalidPriceException(BusinessRuleException):
    """Precio inválido"""
    pass

class OrderAlreadyShippedException(BusinessRuleException):
    """No se puede modificar orden ya enviada"""
    pass

class EntityNotFoundException(DomainException):
    """Entidad no encontrada"""
    pass

class AuthenticationException(DomainException):
    """Error de autenticación"""
    pass

class AuthorizationException(DomainException):
    """Error de autorización"""
    pass

class PaymentProcessingException(DomainException):
    pass