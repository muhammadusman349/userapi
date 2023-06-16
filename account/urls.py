from django.urls import path
# from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (SigninView,UserView ) #ChangePasswordView, PermissionListView,
                   # ResetPasswordStep1View, ResetPasswordStep2View, SigninView,
                   # UserPermissionsView, UserRoleView, UserView)

urlpatterns = [
    path('member/',                     UserView.as_view(),                 name='signup'),
    path('member/<int:id>/',            UserView.as_view(),                 name='user-list-view'),
    path('signin/',                     SigninView.as_view(),               name='signin'),
    # path('reset/password/',             ResetPasswordStep1View.as_view(),   name='reset-password'),
    # path('reset/password/complete/',    ResetPasswordStep2View.as_view(),   name='reset-password-complete'),
    # path('changepassword/',             ChangePasswordView.as_view(),       name='change-password'),
    # path('verify/token/',               TokenVerifyView.as_view(),          name='verify-token'),
    # path('refresh/token/',              TokenRefreshView.as_view(),         name='refresh-token'),
    
]


