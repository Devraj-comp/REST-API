from django.urls import path,include
from rest_framework.routers import DefaultRouter
from restapi import views
from restapi.views import HelloApiView

router = DefaultRouter()
router.register('hello-viewset',views.HelloViewSet,basename='hello-viewset')
router.register('profile',views.UserProfileViewSet)
router.register('feed',views.UserProfileFeedViewSet)
app_name = 'restapi'

urlpatterns = [
    path('hello-view/',views.HelloApiView.as_view()),
    path('login/',views.UserLoginApiView.as_view()),
    path('',include(router.urls))
]