from django.urls import path
from .views import imports, delete, nodes, sales, node_stats

urlpatterns = [
    path('imports', imports),
    path('delete/<str:unit_id>', delete),
    path('nodes/<str:unit_id>', nodes),
    path('node/<str:unit_id>/statistic', node_stats),
    path('sales', sales),

]
