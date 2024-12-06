from alpaka.alpaka import Alpaka
from herre_next import Herre
from fakts_next import Fakts
from typing import Optional

from arkitekt_next.base_models import Manifest

from arkitekt_next.service_registry import (
    BaseArkitektService,
    Params,
)
from arkitekt_next.base_models import Requirement


class ArkitektAlpaka(Alpaka):
    endpoint_url: str = "fake_url"
    fakts: Fakts
    herre: Herre

    async def aconnect(self, *args, **kwargs):
        endpoint_url = await self.fakts.get("alpaka.endpoint_url")
        self.endpoint_url = endpoint_url
        await super().aconnect(*args, **kwargs)

    class Config:
        arbitrary_types_allowed = True

class AlpakaService(BaseArkitektService):


    def get_service_name(self):
        return "alpaka"

    def build_service(self, fakts: Fakts, herre: Herre, params: Params, manifest: Manifest):
         return ArkitektAlpaka(
            fakts=fakts,
            herre=herre,
        )

    def get_requirements(self):
        return [
            Requirement(
            key="alpaka",
            service="io.ollama.ollama",
            description="An instance of Ollama to chat with",
        )
        ]

    def get_graphql_schema(self):
        return None



def build_services():
    return [AlpakaService()]