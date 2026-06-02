import pytest
from src.services.notificacao_service import NotificacaoService
from src.models.notificacao import Notificacao


class TestNotificacaoService:
    @pytest.fixture
    def service(self):
        return NotificacaoService()

    def test_deve_criar_notificacao_com_dados_validos(self, service):
        dto = {"email": "test@email.com", "mensagem": "Bem-vindo!"}

        resultado = service.criar(dto)

        assert resultado.email == "test@email.com"
        assert resultado.status == "ENVIADO"

    def test_deve_lancar_erro_para_email_invalido(self, service):
        dto = {"email": "invalido", "mensagem": "Teste"}

        with pytest.raises(ValueError, match="Email inválido"):
            service.criar(dto)