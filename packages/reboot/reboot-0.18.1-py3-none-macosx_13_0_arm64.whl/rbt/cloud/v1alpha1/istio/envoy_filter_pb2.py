# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rbt/cloud/v1alpha1/istio/envoy_filter.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from rbt.cloud.v1alpha1.istio import envoy_filter_spec_pb2 as rbt_dot_cloud_dot_v1alpha1_dot_istio_dot_envoy__filter__spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n+rbt/cloud/v1alpha1/istio/envoy_filter.proto\x12\x18rbt.cloud.v1alpha1.istio\x1a\x30rbt/cloud/v1alpha1/istio/envoy_filter_spec.proto\"C\n\x0b\x45nvoyFilter\x12\x34\n\x04spec\x18\x01 \x01(\x0b\x32&.istio.networking.v1alpha3.EnvoyFilterb\x06proto3')



_ENVOYFILTER = DESCRIPTOR.message_types_by_name['EnvoyFilter']
EnvoyFilter = _reflection.GeneratedProtocolMessageType('EnvoyFilter', (_message.Message,), {
  'DESCRIPTOR' : _ENVOYFILTER,
  '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_pb2'
  # @@protoc_insertion_point(class_scope:rbt.cloud.v1alpha1.istio.EnvoyFilter)
  })
_sym_db.RegisterMessage(EnvoyFilter)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ENVOYFILTER._serialized_start=123
  _ENVOYFILTER._serialized_end=190
# @@protoc_insertion_point(module_scope)
