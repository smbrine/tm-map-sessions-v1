from uuid import uuid4

from sqlalchemy import select

from app import schemas
from db import models
from db.main import sessionmanager


class SessionManager:
    def __init__(self):
        pass

    async def create_new_session(
        self,
        user_id: int,
        features: list[schemas.Feature],
    ) -> str:
        async with (
            sessionmanager.session() as session
        ):

            # TODO: start a transaction and wrap everything in try except clause.
            try:
                # TODO: create a session with random uuid
                session_uuid = uuid4()
                await models.Session.create(
                    db=session,
                    identifier=session_uuid,
                    user_id=user_id,
                )
                new_features = []
                for feature_data in features:
                    # TODO: check if feature.type is in feature_types table, otherwise default to PointSet
                    feature_type_name = (
                        feature_data.type
                    )
                    stmt = select(
                        models.FeatureType
                    ).where(
                        models.FeatureType.name
                        == feature_type_name
                    )
                    result = (
                        await session.execute(
                            stmt
                        )
                    )
                    feature_type = (
                        result.scalar_one_or_none()
                    )
                    if not feature_type:
                        stmt = select(
                            models.FeatureType
                        ).where(
                            models.FeatureType.name
                            == "PointSet"
                        )
                        result = (
                            await session.execute(
                                stmt
                            )
                        )
                        feature_type = (
                            result.scalar_one_or_none()
                        )

                        if not feature_type:
                            feature_type = await models.FeatureType.create(
                                db=session,
                                id=0,
                                name="PointSet",
                            )
                    feature_type_id = (
                        feature_type.id
                    )

                    # TODO: create a feature with the created geometry

                    # Create a geometry for the feature

                    new_geometry_id = uuid4()
                    new_points = []
                    # Generate UUIDs for each point and create point records
                    new_geometry = await models.Geometry.create(
                        identifier=new_geometry_id,
                        db=session,
                    )
                    for (
                        point_data
                    ) in (
                        feature_data.geometry.points
                    ):
                        new_points.append(
                            await models.Point.create(
                                db=session,
                                latitude=point_data.latitude,
                                longitude=point_data.longitude,
                                geometry_id=new_geometry_id,
                            )
                        )
                    # new_geometry.points = new_points
                    new_feature = await models.Feature.create(
                        db=session,
                        session_id=session_uuid,
                        type_id=feature_type_id,
                        name=feature_data.name,
                        geometry_id=new_geometry_id,
                        geometry=new_geometry,
                    )
                    new_features.append(
                        new_feature
                    )
                    await session.flush()  # Ensure the new geometry is flushed to get its ID

                # new_session.features = features_in_db
                await session.commit()

                # TODO: return session_uuid or rollback in case of exception and reraise it
                return str(session_uuid)
            except Exception as e:
                await session.rollback()
                raise e

    async def get_session(
        self, session_id
    ) -> schemas.SessionResponse:
        async with (
            sessionmanager.session() as session
        ):
            session_in_db = (
                await models.Session.get(
                    session, session_id
                )
            )
            return schemas.SessionResponse(
                features=[
                    schemas.Feature(
                        geometry=schemas.Geometry(
                            points=[
                                schemas.Point(
                                    latitude=point.latitude,
                                    longitude=point.longitude,
                                )
                                for point in feature.geometry.points
                            ]
                        ),
                        type=feature.type.name,
                        name=feature.name,
                    )
                    for feature in session_in_db.features
                ]
            )
