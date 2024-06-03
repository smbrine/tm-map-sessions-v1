import asyncio
import logging

from app import schemas, settings
from db.main import sessionmanager
from proto import (
    map_sessions_service_pb2,
    map_sessions_service_pb2_grpc,
)
from tools import SessionManager
from grpc_reflection.v1alpha import reflection
from grpc import aio as grpc_aio


logging.basicConfig(level=logging.DEBUG)
sm = SessionManager()

sessionmanager.init(settings.POSTGRES_URL)


class MapSessionsServiceServicer(
    map_sessions_service_pb2_grpc.MapSessionsServiceServicer
):
    async def CreateSession(
        self, request, context
    ):
        features = [
            schemas.Feature(
                geometry=schemas.Geometry(
                    points=[
                        schemas.Point(
                            latitude=point.latitude,
                            longitude=point.longitude,
                        )
                        for point in feature.geometry.points
                    ],
                ),
                name=feature.name,
                type=feature.type,
            )
            for feature in request.features
        ]

        session_uuid = (
            await sm.create_new_session(
                request.user_id, features
            )
        )

        return map_sessions_service_pb2.CreateSessionResponse(
            session_uuid=session_uuid
        )

    async def GetSession(self, request, context):
        session = await sm.get_session(
            request.session_id
        )
        return map_sessions_service_pb2.GetSessionResponse(
            features=[
                map_sessions_service_pb2.Feature(
                    name=feature.name,
                    type=feature.type,
                    geometry=map_sessions_service_pb2.Geometry(
                        points=[
                            map_sessions_service_pb2.Point(
                                latitude=point.latitude,
                                longitude=point.longitude,
                            )
                            for point in feature.geometry.points
                        ]
                    ),
                )
                for feature in session.features
            ]
        )


async def serve():

    server = grpc_aio.server()
    map_sessions_service_pb2_grpc.add_MapSessionsServiceServicer_to_server(
        MapSessionsServiceServicer(),
        server,
    )
    listen_addr = "[::]:50051"
    service_names = (
        map_sessions_service_pb2.DESCRIPTOR.services_by_name[
            "MapSessionsService"
        ].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(
        service_names, server
    )

    server.add_insecure_port(listen_addr)
    await server.start()
    try:
        await server.wait_for_termination()
    finally:
        await server.stop(0)


if __name__ == "__main__":
    asyncio.run(serve())
