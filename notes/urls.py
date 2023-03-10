from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('hello/', views.hello),
    path('category_<int:category_id>/', views.category_detail, name='category_detail'),
    path('note_<int:note_id>/', views.note_detail, name='note_detail'),
    path('new_note/', views.new_note, name='new_note'),
    path('note_<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('note_<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('categories/', views.categories, name='categories'),
    path('search/', views.search_notes, name='search_notes'),
    path('filter/', views.filtered_results, name='filtered'),
    path('acc/', include('django.contrib.auth.urls')),
    path('acc/registration/', views.registration, name='registration'),
]
