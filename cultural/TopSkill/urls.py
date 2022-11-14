from django.urls import path, include, re_path
from . import views

app_name = 'TopSkill'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path(r'students/', views.studentsView, name='students'),
    path(r'search_student/', views.autocomplete, name='search_student'),
    path(r'submit_student/', views.submit_student, name='submit_student'),
    path(r'detail/<uuid:pk>/', views.student_detail, name='student_detail'),
    path(r'detail/<uuid:user_id>/document_score/<int:doc_id>/score', views.document_score, name='document_score'),
    path(r'tsdelete/<uuid:pk>', views.student_delete, name='student_delete'),
    path(r'detail/document_delete/<int:pk>/delete', views.document_delete, name='document_delete'),
    # path('detail/document_delete/<int:pk>/delete', views.DocumentDelete.as_view(), name='document_delete'),
    path(r'detail/download_file/<int:file_id>/download', views.download_file, name='download_file'),
    # path('test', views.levelindex, name='test')
    path(r'detail/<int:id>/description/', views.description, name='description')
]
