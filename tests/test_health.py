"""Teste do endpoint raiz."""


class TestRoot:
    def test_health_check(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome to API!"}
