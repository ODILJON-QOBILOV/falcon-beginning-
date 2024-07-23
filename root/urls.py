from django.contrib import admin
from root import settings
from django.conf.urls.static import static
from django.urls import path
from apps.views import ProductDetailView, ProfileView, SettingsView, index, ProductListView, SignupView, UserLoginView, \
    UserLogoutView, WishListView, WishlistTemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", ProductListView.as_view(), name="products"),
    path("product/<int:pk>", ProductDetailView.as_view(), name="product"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", SettingsView.as_view(), name="settings"),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('wishlist/', WishlistTemplateView.as_view(), name='wishlist'),
    path('like/<int:pk>', WishListView.as_view(), name='like')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    