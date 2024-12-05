from ....assinatura import Assinador
from zeep.plugins import HistoryPlugin
from zeep import Client, Transport, Settings
from requests import Session
from .pedido import Pedido
from lxml.etree import tostring, fromstring
from pathlib import Path
from tempfile import mktemp
from .envio_rps import EnvioRPS, RetornoEnvioRps
from .consulta_cnpj import ConsultaCNPJ, RetornoConsultaCNPJ
from .cancelamento_nfe import CancelamentoNFe, RetornoCancelamentoNFe


class Cliente:
    assinador: Assinador

    def __init__(self, caminho_pfx: Path, senha_pfx: str):
        self.assinador = Assinador(caminho_pfx, senha_pfx)

    def executar(self, pedido: Pedido) -> str:
        try:
            history = HistoryPlugin()
            keyfile = Path(mktemp())
            keyfile.write_bytes(self.assinador.private_key_pem_bytes)
            certfile = Path(mktemp())
            certfile.write_bytes(self.assinador.cert_pem_bytes)
            url = "https://nfe.prefeitura.sp.gov.br/ws/lotenfe.asmx?WSDL"
            xml = pedido.gerar_xml(self.assinador)
            session = Session()
            session.cert = (certfile, keyfile)
            settings = Settings(strict=True, xml_huge_tree=True)
            transport = Transport(session=session, cache=None)
            client = Client(
                url, transport=transport, settings=settings, plugins=[history]
            )
            signed_xml = self.assinador.assinar_xml(xml)

            response: str = getattr(client.service, pedido.__class__.__name__)(
                1, tostring(signed_xml, encoding=str)
            )

            return fromstring(response.encode("utf-8"))
        finally:
            keyfile.unlink()
            certfile.unlink()

    def gerar_nota(self, pedido: EnvioRPS) -> RetornoEnvioRps:
        return RetornoEnvioRps.ler_xml(self.executar(pedido))

    def consultar_cnpj(self, pedido: ConsultaCNPJ) -> RetornoConsultaCNPJ:
        return RetornoConsultaCNPJ.ler_xml(self.executar(pedido))

    def cancelar_nota(self, pedido: CancelamentoNFe) -> RetornoCancelamentoNFe:
        return RetornoCancelamentoNFe.ler_xml(self.executar(pedido))
