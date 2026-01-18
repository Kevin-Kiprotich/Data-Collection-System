from django.urls import path
from .views import BulkSubmissionView

urlpatterns = [
    path('submissions/bulk/', BulkSubmissionView.as_view(), name='bulk-submission'),
]