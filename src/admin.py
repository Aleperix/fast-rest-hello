from src.models.user import UserAdmin, BlockedTokenAdmin
from src.models.locations import CountryAdmin, StateAdmin

def init(admin_backend):
    admin_backend.add_view(UserAdmin)
    admin_backend.add_view(BlockedTokenAdmin)

    admin_backend.add_view(CountryAdmin)
    admin_backend.add_view(StateAdmin)