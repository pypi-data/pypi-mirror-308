# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/annotations/resource.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n envoy/annotations/resource.proto\x12\x11\x65nvoy.annotations\x1a google/protobuf/descriptor.proto\"\"\n\x12ResourceAnnotation\x12\x0c\n\x04type\x18\x01 \x01(\t:[\n\x08resource\x12\x1f.google.protobuf.ServiceOptions\x18\xc1\xe4\xb2~ \x01(\x0b\x32%.envoy.annotations.ResourceAnnotationB:Z8github.com/envoyproxy/go-control-plane/envoy/annotationsb\x06proto3')


RESOURCE_FIELD_NUMBER = 265073217
resource = DESCRIPTOR.extensions_by_name['resource']

_RESOURCEANNOTATION = DESCRIPTOR.message_types_by_name['ResourceAnnotation']
ResourceAnnotation = _reflection.GeneratedProtocolMessageType('ResourceAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _RESOURCEANNOTATION,
  '__module__' : 'envoy.annotations.resource_pb2'
  # @@protoc_insertion_point(class_scope:envoy.annotations.ResourceAnnotation)
  })
_sym_db.RegisterMessage(ResourceAnnotation)

if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.ServiceOptions.RegisterExtension(resource)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z8github.com/envoyproxy/go-control-plane/envoy/annotations'
  _RESOURCEANNOTATION._serialized_start=89
  _RESOURCEANNOTATION._serialized_end=123
# @@protoc_insertion_point(module_scope)
