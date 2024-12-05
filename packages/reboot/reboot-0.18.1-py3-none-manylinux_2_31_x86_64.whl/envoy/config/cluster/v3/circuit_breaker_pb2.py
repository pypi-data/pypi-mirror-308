# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/config/cluster/v3/circuit_breaker.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from envoy.config.core.v3 import base_pb2 as envoy_dot_config_dot_core_dot_v3_dot_base__pb2
from envoy.type.v3 import percent_pb2 as envoy_dot_type_dot_v3_dot_percent__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n-envoy/config/cluster/v3/circuit_breaker.proto\x12\x17\x65nvoy.config.cluster.v3\x1a\x1f\x65nvoy/config/core/v3/base.proto\x1a\x1b\x65nvoy/type/v3/percent.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\x1a\x17validate/validate.proto\"\xaa\x07\n\x0f\x43ircuitBreakers\x12G\n\nthresholds\x18\x01 \x03(\x0b\x32\x33.envoy.config.cluster.v3.CircuitBreakers.Thresholds\x12P\n\x13per_host_thresholds\x18\x02 \x03(\x0b\x32\x33.envoy.config.cluster.v3.CircuitBreakers.Thresholds\x1a\xce\x05\n\nThresholds\x12\x41\n\x08priority\x18\x01 \x01(\x0e\x32%.envoy.config.core.v3.RoutingPriorityB\x08\xfa\x42\x05\x82\x01\x02\x10\x01\x12\x35\n\x0fmax_connections\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12:\n\x14max_pending_requests\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x32\n\x0cmax_requests\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x31\n\x0bmax_retries\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12U\n\x0cretry_budget\x18\x08 \x01(\x0b\x32?.envoy.config.cluster.v3.CircuitBreakers.Thresholds.RetryBudget\x12\x17\n\x0ftrack_remaining\x18\x06 \x01(\x08\x12:\n\x14max_connection_pools\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x1a\xbe\x01\n\x0bRetryBudget\x12.\n\x0e\x62udget_percent\x18\x01 \x01(\x0b\x32\x16.envoy.type.v3.Percent\x12;\n\x15min_retry_concurrency\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value:B\x9a\xc5\x88\x1e=\n;envoy.api.v2.cluster.CircuitBreakers.Thresholds.RetryBudget:6\x9a\xc5\x88\x1e\x31\n/envoy.api.v2.cluster.CircuitBreakers.Thresholds:+\x9a\xc5\x88\x1e&\n$envoy.api.v2.cluster.CircuitBreakersB\x90\x01\n%io.envoyproxy.envoy.config.cluster.v3B\x13\x43ircuitBreakerProtoP\x01ZHgithub.com/envoyproxy/go-control-plane/envoy/config/cluster/v3;clusterv3\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_CIRCUITBREAKERS = DESCRIPTOR.message_types_by_name['CircuitBreakers']
_CIRCUITBREAKERS_THRESHOLDS = _CIRCUITBREAKERS.nested_types_by_name['Thresholds']
_CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET = _CIRCUITBREAKERS_THRESHOLDS.nested_types_by_name['RetryBudget']
CircuitBreakers = _reflection.GeneratedProtocolMessageType('CircuitBreakers', (_message.Message,), {

  'Thresholds' : _reflection.GeneratedProtocolMessageType('Thresholds', (_message.Message,), {

    'RetryBudget' : _reflection.GeneratedProtocolMessageType('RetryBudget', (_message.Message,), {
      'DESCRIPTOR' : _CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET,
      '__module__' : 'envoy.config.cluster.v3.circuit_breaker_pb2'
      # @@protoc_insertion_point(class_scope:envoy.config.cluster.v3.CircuitBreakers.Thresholds.RetryBudget)
      })
    ,
    'DESCRIPTOR' : _CIRCUITBREAKERS_THRESHOLDS,
    '__module__' : 'envoy.config.cluster.v3.circuit_breaker_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.cluster.v3.CircuitBreakers.Thresholds)
    })
  ,
  'DESCRIPTOR' : _CIRCUITBREAKERS,
  '__module__' : 'envoy.config.cluster.v3.circuit_breaker_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.cluster.v3.CircuitBreakers)
  })
_sym_db.RegisterMessage(CircuitBreakers)
_sym_db.RegisterMessage(CircuitBreakers.Thresholds)
_sym_db.RegisterMessage(CircuitBreakers.Thresholds.RetryBudget)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n%io.envoyproxy.envoy.config.cluster.v3B\023CircuitBreakerProtoP\001ZHgithub.com/envoyproxy/go-control-plane/envoy/config/cluster/v3;clusterv3\272\200\310\321\006\002\020\002'
  _CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET._options = None
  _CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET._serialized_options = b'\232\305\210\036=\n;envoy.api.v2.cluster.CircuitBreakers.Thresholds.RetryBudget'
  _CIRCUITBREAKERS_THRESHOLDS.fields_by_name['priority']._options = None
  _CIRCUITBREAKERS_THRESHOLDS.fields_by_name['priority']._serialized_options = b'\372B\005\202\001\002\020\001'
  _CIRCUITBREAKERS_THRESHOLDS._options = None
  _CIRCUITBREAKERS_THRESHOLDS._serialized_options = b'\232\305\210\0361\n/envoy.api.v2.cluster.CircuitBreakers.Thresholds'
  _CIRCUITBREAKERS._options = None
  _CIRCUITBREAKERS._serialized_options = b'\232\305\210\036&\n$envoy.api.v2.cluster.CircuitBreakers'
  _CIRCUITBREAKERS._serialized_start=260
  _CIRCUITBREAKERS._serialized_end=1198
  _CIRCUITBREAKERS_THRESHOLDS._serialized_start=435
  _CIRCUITBREAKERS_THRESHOLDS._serialized_end=1153
  _CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET._serialized_start=907
  _CIRCUITBREAKERS_THRESHOLDS_RETRYBUDGET._serialized_end=1097
# @@protoc_insertion_point(module_scope)
