from fluss_next.fluss import Fluss
from fluss_next.rath import FlussLinkComposition, FlussRath
from rath.links.split import SplitLink
from fakts_next.contrib.rath.aiohttp import FaktsAIOHttpLink
from fakts_next.contrib.rath.graphql_ws import FaktsGraphQLWSLink
from herre_next.contrib.rath.auth_link import HerreAuthLink
from graphql import OperationType
from herre_next import Herre
from fakts_next import Fakts

from arkitekt_next.base_models import Manifest

from arkitekt_next.service_registry import (
    Params,
)
from arkitekt_next.base_models import Requirement


def init_services(service_builder_registry):

    class ArkitektNextFluss(Fluss):
        rath: FlussRath

    def build_arkitekt_next_fluss(
        fakts: Fakts, herre: Herre, params: Params, manifest: Manifest
    ):
        return ArkitektNextFluss(
            rath=FlussRath(
                link=FlussLinkComposition(
                    auth=HerreAuthLink(herre=herre),
                    split=SplitLink(
                        left=FaktsAIOHttpLink(
                            fakts_group="fluss", fakts=fakts, endpoint_url="FAKE_URL"
                        ),
                        right=FaktsGraphQLWSLink(
                            fakts_group="fluss", fakts=fakts, ws_endpoint_url="FAKE_URL"
                        ),
                        split=lambda o: o.node.operation != OperationType.SUBSCRIPTION,
                    ),
                )
            )
        )

    service_builder_registry.register(
        "fluss",
        build_arkitekt_next_fluss,
        Requirement(
            key="fluss",
            service="live.arkitekt.fluss",
            description="An instance of ArkitektNext fluss to retrieve graphs from",
        ),
    )
