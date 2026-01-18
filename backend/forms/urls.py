from django.urls import path
from .views.submissions import BulkSubmissionView

urlpatterns = [
    path('submissions/bulk/', BulkSubmissionView.as_view(), name='bulk-submission'),
]