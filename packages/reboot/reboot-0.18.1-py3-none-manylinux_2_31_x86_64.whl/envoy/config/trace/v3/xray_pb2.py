# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/config/trace/v3/xray.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from envoy.config.core.v3 import address_pb2 as envoy_dot_config_dot_core_dot_v3_dot_address__pb2
from envoy.config.core.v3 import base_pb2 as envoy_dot_config_dot_core_dot_v3_dot_base__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from udpa.annotations import migrate_pb2 as udpa_dot_annotations_dot_migrate__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n envoy/config/trace/v3/xray.proto\x12\x15\x65nvoy.config.trace.v3\x1a\"envoy/config/core/v3/address.proto\x1a\x1f\x65nvoy/config/core/v3/base.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1eudpa/annotations/migrate.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\x1a\x17validate/validate.proto\"\xe9\x02\n\nXRayConfig\x12<\n\x0f\x64\x61\x65mon_endpoint\x18\x01 \x01(\x0b\x32#.envoy.config.core.v3.SocketAddress\x12\x1d\n\x0csegment_name\x18\x02 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12@\n\x16sampling_rule_manifest\x18\x03 \x01(\x0b\x32 .envoy.config.core.v3.DataSource\x12G\n\x0esegment_fields\x18\x04 \x01(\x0b\x32/.envoy.config.trace.v3.XRayConfig.SegmentFields\x1a\x45\n\rSegmentFields\x12\x0e\n\x06origin\x18\x01 \x01(\t\x12$\n\x03\x61ws\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct:,\x9a\xc5\x88\x1e\'\n%envoy.config.trace.v2alpha.XRayConfigB\xad\x01\n#io.envoyproxy.envoy.config.trace.v3B\tXrayProtoP\x01ZDgithub.com/envoyproxy/go-control-plane/envoy/config/trace/v3;tracev3\xf2\x98\xfe\x8f\x05\'\x12%envoy.extensions.tracers.xray.v4alpha\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_XRAYCONFIG = DESCRIPTOR.message_types_by_name['XRayConfig']
_XRAYCONFIG_SEGMENTFIELDS = _XRAYCONFIG.nested_types_by_name['SegmentFields']
XRayConfig = _reflection.GeneratedProtocolMessageType('XRayConfig', (_message.Message,), {

  'SegmentFields' : _reflection.GeneratedProtocolMessageType('SegmentFields', (_message.Message,), {
    'DESCRIPTOR' : _XRAYCONFIG_SEGMENTFIELDS,
    '__module__' : 'envoy.config.trace.v3.xray_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.trace.v3.XRayConfig.SegmentFields)
    })
  ,
  'DESCRIPTOR' : _XRAYCONFIG,
  '__module__' : 'envoy.config.trace.v3.xray_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.trace.v3.XRayConfig)
  })
_sym_db.RegisterMessage(XRayConfig)
_sym_db.RegisterMessage(XRayConfig.SegmentFields)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#io.envoyproxy.envoy.config.trace.v3B\tXrayProtoP\001ZDgithub.com/envoyproxy/go-control-plane/envoy/config/trace/v3;tracev3\362\230\376\217\005\'\022%envoy.extensions.tracers.xray.v4alpha\272\200\310\321\006\002\020\002'
  _XRAYCONFIG.fields_by_name['segment_name']._options = None
  _XRAYCONFIG.fields_by_name['segment_name']._serialized_options = b'\372B\004r\002\020\001'
  _XRAYCONFIG._options = None
  _XRAYCONFIG._serialized_options = b'\232\305\210\036\'\n%envoy.config.trace.v2alpha.XRayConfig'
  _XRAYCONFIG._serialized_start=282
  _XRAYCONFIG._serialized_end=643
  _XRAYCONFIG_SEGMENTFIELDS._serialized_start=528
  _XRAYCONFIG_SEGMENTFIELDS._serialized_end=597
# @@protoc_insertion_point(module_scope)
