from rest_framework import status
from rest_framework.test import APITestCase

from .models import Estatus, Guia

DATOS = {
    "trackingNumber": "he-001",
    "recipient": "Ana López",
    "origin": "Puebla",
    "destination": "Ciudad de México",
    "createdAt": "2026-10-24",
    "currentStatus": "Pendiente",
}


class GuiaEndpointsTests(APITestCase):
    def crear(self, **cambios):
        return self.client.post("/api/crear-guia", {**DATOS, **cambios}, format="json")

    def test_crear_guia(self):
        response = self.crear(updatedBy="operador1")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["trackingNumber"], "HE-001")
        self.assertEqual(len(response.data["history"]), 1)
        self.assertEqual(Estatus.objects.get().updatedBy, "operador1")

    def test_crear_guia_repetida(self):
        self.crear()
        response = self.crear(trackingNumber=" He-001 ")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["trackingNumber"][0], "Ya existe una guía con este número.")

    def test_crear_guia_con_campos_vacios(self):
        response = self.client.post("/api/crear-guia", {"trackingNumber": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        for campo in ["trackingNumber", "origin", "destination"]:
            self.assertIn(campo, response.data)

    def test_estado_invalido(self):
        response = self.crear(currentStatus="Perdida")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_obtener_guia(self):
        guia_id = self.crear().data["id"]
        response = self.client.get(f"/api/obtener-guia/{guia_id}")
        self.assertEqual(response.data["destination"], "Ciudad de México")

    def test_obtener_guia_que_no_existe(self):
        response = self.client.get("/api/obtener-guia/999")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_listar_guias(self):
        self.crear()
        self.crear(trackingNumber="HE-002")
        response = self.client.get("/api/guias")
        self.assertEqual([g["trackingNumber"] for g in response.data], ["HE-002", "HE-001"])

    def test_actualizar_guia_con_put(self):
        guia_id = self.crear().data["id"]
        datos = {**DATOS, "destination": "Monterrey", "currentStatus": "En tránsito"}
        response = self.client.put(f"/api/actualizar-guia/{guia_id}", datos, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        guia = Guia.objects.get()
        self.assertEqual((guia.destination, guia.currentStatus), ("Monterrey", "En tránsito"))
        self.assertEqual(list(guia.history.values_list("status", flat=True)), ["Pendiente", "En tránsito"])

    def test_actualizar_solo_estado_con_patch(self):
        guia_id = self.crear().data["id"]
        url = f"/api/actualizar-guia/{guia_id}"
        self.client.patch(url, {"currentStatus": "En tránsito"}, format="json")
        self.client.patch(url, {"currentStatus": "En tránsito"}, format="json")
        response = self.client.patch(url, {"currentStatus": "Entregada"}, format="json")
        self.assertEqual(response.data["currentStatus"], "Entregada")
        self.assertEqual(len(response.data["history"]), 3)

    def test_eliminar_guia(self):
        guia_id = self.crear().data["id"]
        response = self.client.delete(f"/api/eliminar-guia/{guia_id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Guia.objects.exists())
        self.assertFalse(Estatus.objects.exists())

    def test_metodo_incorrecto(self):
        response = self.client.get("/api/crear-guia")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
