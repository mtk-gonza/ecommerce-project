from app.domain.enums.role_type import RoleType

ROLES = [
    {
        'name': RoleType.ROOT.value, 
        'description':'System Administrator and all permissions'
    },
    {
        'name': RoleType.ADMIN.value, 
        'description':'System Administrator'
    },
    {
        'name': RoleType.EDITOR.value, 
        'description':'User with editing permissions'
    },
    {
        'name': RoleType.USER.value, 
        'description':'Basic User'
    },
    {
        'name': RoleType.GUEST.value, 
        'description':'Guest User'
    }
]