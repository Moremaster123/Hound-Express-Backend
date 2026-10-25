from rest_framework import viewsets

from .models import Guia
from .serializers import GuiaSerializer


class GuiaViewSet(viewsets.ModelViewSet):
    queryset = Guia.objects.prefetch_related("history").order_by("-id")
    serializer_class = GuiaSerializer
