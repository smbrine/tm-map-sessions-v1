from datetime import datetime
from typing import Any
from uuid import uuid4

import sqlalchemy
from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UUID,
    and_,
    select,
)
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    as_declarative,
    declared_attr,
    relationship,
    selectinload,
)


from db.main import Base


class BaseModel(Base):
    __abstract__ = True
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    created_at = Column(
        DateTime, default=datetime.now
    )

    @classmethod
    async def create(
        cls,
        db: AsyncSession,
        identifier=None,
        created_at=None,
        **kwargs,
    ):
        if not identifier:
            identifier = uuid4()
        if not created_at:
            created_at = datetime.now()

        transaction = cls(
            id=identifier,
            created_at=created_at,
            **kwargs,
        )
        try:
            db.add(transaction)
            await db.commit()
            await db.refresh(transaction)
        except IntegrityError as e:
            await db.rollback()
            raise RuntimeError(e) from e

        return transaction

    @classmethod
    async def get(
        cls, db: AsyncSession, identifier: str
    ):
        try:
            transaction = await db.get(
                cls, identifier
            )
        except NoResultFound:
            return None
        return transaction

    @classmethod
    async def get_all(
        cls,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ):
        stmt = (
            select(cls).offset(skip).limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at})>"


class Session(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(BigInteger, nullable=False)
    features = relationship(
        "Feature",
        back_populates="session",
        lazy="joined",
        uselist=True,
    )

    def __repr__(self):
        return f"<Session(id={self.id}, user_id={self.user_id})>"


class Feature(BaseModel):
    __tablename__ = "features"

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("sessions.id"),
        nullable=False,
    )
    type_id = Column(
        Integer,
        ForeignKey("feature_types.id"),
        nullable=False,
        index=True,
    )
    session = relationship(
        "Session", back_populates="features"
    )
    type = relationship(
        "FeatureType",
        back_populates="features",
        lazy="joined",
    )
    geometry = relationship(
        "Geometry",
        back_populates="feature",
        lazy="joined",
        uselist=False,
    )
    name = Column(
        String,
        nullable=True,
    )
    geometry_id = Column(
        UUID(as_uuid=True),
        ForeignKey("geometries.id"),
        nullable=False,
    )

    def __repr__(self):
        return f"<Feature(id={str(self.id)}, session_id={self.session_id}, type_id={self.type_id})>"


class Geometry(BaseModel):
    __tablename__ = "geometries"

    points = relationship(
        "Point",
        back_populates="geometry",
        cascade="all, delete-orphan",
        uselist=True,
        lazy="joined",
    )

    feature = relationship(
        "Feature",
        back_populates="geometry",
        lazy="joined",
    )

    def __repr__(self):
        return f"<Geometry(id={self.id}, feature_id={self.feature.id})>"


class Point(BaseModel):
    __tablename__ = "points"

    geometry_id = Column(
        UUID(as_uuid=True),
        ForeignKey("geometries.id"),
        nullable=False,
    )
    latitude = Column(
        Numeric(7, 4), nullable=False
    )
    longitude = Column(
        Numeric(7, 4), nullable=False
    )

    geometry = relationship(
        "Geometry",
        back_populates="points",
        uselist=False,
    )

    def __repr__(self):
        return f"<Point(id={self.id}, latitude={self.latitude}, longitude={self.longitude}, geometry_id={self.geometry_id})>"


class FeatureType(Base):
    __tablename__ = "feature_types"
    id = Column(Integer, primary_key=True)
    name = Column(
        String(255), nullable=False, unique=True
    )
    features = relationship(
        "Feature", back_populates="type"
    )

    def __repr__(self):
        return f"<FeatureType(id={self.id}, name={self.name})>"
