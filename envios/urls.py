from django.urls import re_path

from .views import GuiaViewSet

listar_guias = GuiaViewSet.as_view({"get": "list"})
crear_guia = GuiaViewSet.as_view({"post": "create"})
obtener_guia = GuiaViewSet.as_view({"get": "retrieve"})
actualizar_guia = GuiaViewSet.as_view({"put": "update", "patch": "partial_update"})
eliminar_guia = GuiaViewSet.as_view({"delete": "destroy"})

urlpatterns = [
    re_path(r"^guias/?$", listar_guias, name="listar-guias"),
    re_path(r"^crear-guia/?$", crear_guia, name="crear-guia"),
    re_path(r"^obtener-guia/(?P<pk>\d+)/?$", obtener_guia, name="obtener-guia"),
    re_path(r"^actualizar-guia/(?P<pk>\d+)/?$", actualizar_guia, name="actualizar-guia"),
    re_path(r"^eliminar-guia/(?P<pk>\d+)/?$", eliminar_guia, name="eliminar-guia"),
]
