from django.urls import path, include, re_path
from . import views

app_name = 'TopSkill'
urlpatterns = [
    path('', views.indexView, name='index'),
    path(r'student/', views.autocomplete, name='student'),
    path(r'submit_student/', views.submit_student, name='submit_student'),
    path(r'detail/<uuid:pk>/', views.student_detail, name='student_detail'),
    path(r'detail/<uuid:user_id>/document_score/<int:doc_id>/score', views.document_score, name='document_score'),
    path(r'tsdelete/<uuid:pk>', views.tsdelete, name='tsdelete'),
    path(r'detail/document_delete/<int:pk>/delete', views.document_delete, name='document_delete'),
    # path('detail/document_delete/<int:pk>/delete', views.DeleteDoc.as_view(), name='document_delete'),
    path(r'detail/download_file/<int:file_id>/download', views.download_file, name='download_file'),
    # path('test', views.levelindex, name='test')
]
