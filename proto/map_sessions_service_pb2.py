# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/map_sessions_service.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import (
    descriptor as _descriptor,
)
from google.protobuf import (
    descriptor_pool as _descriptor_pool,
)
from google.protobuf import (
    symbol_database as _symbol_database,
)
from google.protobuf.internal import (
    builder as _builder,
)

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n proto/map_sessions_service.proto\x12\x0bmapsessions"O\n\x14\x43reateSessionRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x03\x12&\n\x08\x66\x65\x61tures\x18\x02 \x03(\x0b\x32\x14.mapsessions.Feature"-\n\x15\x43reateSessionResponse\x12\x14\n\x0csession_uuid\x18\x01 \x01(\t"N\n\x07\x46\x65\x61ture\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\'\n\x08geometry\x18\x02 \x01(\x0b\x32\x15.mapsessions.Geometry\x12\x0c\n\x04name\x18\x03 \x01(\t".\n\x08Geometry\x12"\n\x06points\x18\x01 \x03(\x0b\x32\x12.mapsessions.Point",\n\x05Point\x12\x10\n\x08latitude\x18\x01 \x01(\x01\x12\x11\n\tlongitude\x18\x02 \x01(\x01"\'\n\x11GetSessionRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t"<\n\x12GetSessionResponse\x12&\n\x08\x66\x65\x61tures\x18\x01 \x03(\x0b\x32\x14.mapsessions.Feature2\xbf\x01\n\x12MapSessionsService\x12X\n\rCreateSession\x12!.mapsessions.CreateSessionRequest\x1a".mapsessions.CreateSessionResponse"\x00\x12O\n\nGetSession\x12\x1e.mapsessions.GetSessionRequest\x1a\x1f.mapsessions.GetSessionResponse"\x00\x62\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(
    DESCRIPTOR, _globals
)
_builder.BuildTopDescriptorsAndMessages(
    DESCRIPTOR,
    "proto.map_sessions_service_pb2",
    _globals,
)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals[
        "_CREATESESSIONREQUEST"
    ]._serialized_start = 49
    _globals[
        "_CREATESESSIONREQUEST"
    ]._serialized_end = 128
    _globals[
        "_CREATESESSIONRESPONSE"
    ]._serialized_start = 130
    _globals[
        "_CREATESESSIONRESPONSE"
    ]._serialized_end = 175
    _globals["_FEATURE"]._serialized_start = 177
    _globals["_FEATURE"]._serialized_end = 255
    _globals["_GEOMETRY"]._serialized_start = 257
    _globals["_GEOMETRY"]._serialized_end = 303
    _globals["_POINT"]._serialized_start = 305
    _globals["_POINT"]._serialized_end = 349
    _globals[
        "_GETSESSIONREQUEST"
    ]._serialized_start = 351
    _globals[
        "_GETSESSIONREQUEST"
    ]._serialized_end = 390
    _globals[
        "_GETSESSIONRESPONSE"
    ]._serialized_start = 392
    _globals[
        "_GETSESSIONRESPONSE"
    ]._serialized_end = 452
    _globals[
        "_MAPSESSIONSSERVICE"
    ]._serialized_start = 455
    _globals[
        "_MAPSESSIONSSERVICE"
    ]._serialized_end = 646
# @@protoc_insertion_point(module_scope)
