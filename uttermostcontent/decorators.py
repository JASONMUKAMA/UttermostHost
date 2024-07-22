from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


def non_staff_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_staff:
            raise PermissionDenied("Staff members are not allowed to access this page!")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
