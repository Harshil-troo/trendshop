from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



class CustomPermissionRequired(PermissionRequiredMixin):
    """
    This class will give custom permissions.
    """
    permission_required = ('user.is_staff', 'user.is_superuser')