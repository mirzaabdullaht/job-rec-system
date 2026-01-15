from django.urls import path
from .views import JobListCreateView, JobDetailView, RecommendationsView

urlpatterns = [
    path('', JobListCreateView.as_view(), name='jobs-list-create'),
    path('<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('recommendations/', RecommendationsView.as_view(), name='job-recommendations'),
]
