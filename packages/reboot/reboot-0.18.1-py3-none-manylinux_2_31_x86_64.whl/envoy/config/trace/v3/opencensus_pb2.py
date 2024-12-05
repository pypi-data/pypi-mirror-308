# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/config/trace/v3/opencensus.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from envoy.config.core.v3 import grpc_service_pb2 as envoy_dot_config_dot_core_dot_v3_dot_grpc__service__pb2
from opencensus.proto.trace.v1 import trace_config_pb2 as opencensus_dot_proto_dot_trace_dot_v1_dot_trace__config__pb2
from envoy.annotations import deprecation_pb2 as envoy_dot_annotations_dot_deprecation__pb2
from udpa.annotations import migrate_pb2 as udpa_dot_annotations_dot_migrate__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&envoy/config/trace/v3/opencensus.proto\x12\x15\x65nvoy.config.trace.v3\x1a\'envoy/config/core/v3/grpc_service.proto\x1a,opencensus/proto/trace/v1/trace_config.proto\x1a#envoy/annotations/deprecation.proto\x1a\x1eudpa/annotations/migrate.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\"\xa7\x06\n\x10OpenCensusConfig\x12<\n\x0ctrace_config\x18\x01 \x01(\x0b\x32&.opencensus.proto.trace.v1.TraceConfig\x12\x1f\n\x17stdout_exporter_enabled\x18\x02 \x01(\x08\x12$\n\x1cstackdriver_exporter_enabled\x18\x03 \x01(\x08\x12\x1e\n\x16stackdriver_project_id\x18\x04 \x01(\t\x12\x1b\n\x13stackdriver_address\x18\n \x01(\t\x12\x43\n\x18stackdriver_grpc_service\x18\r \x01(\x0b\x32!.envoy.config.core.v3.GrpcService\x12,\n\x17zipkin_exporter_enabled\x18\x05 \x01(\x08\x42\x0b\x18\x01\x92\xc7\x86\xd8\x04\x03\x33.0\x12\x1f\n\nzipkin_url\x18\x06 \x01(\tB\x0b\x18\x01\x92\xc7\x86\xd8\x04\x03\x33.0\x12 \n\x18ocagent_exporter_enabled\x18\x0b \x01(\x08\x12\x17\n\x0focagent_address\x18\x0c \x01(\t\x12?\n\x14ocagent_grpc_service\x18\x0e \x01(\x0b\x32!.envoy.config.core.v3.GrpcService\x12T\n\x16incoming_trace_context\x18\x08 \x03(\x0e\x32\x34.envoy.config.trace.v3.OpenCensusConfig.TraceContext\x12T\n\x16outgoing_trace_context\x18\t \x03(\x0e\x32\x34.envoy.config.trace.v3.OpenCensusConfig.TraceContext\"`\n\x0cTraceContext\x12\x08\n\x04NONE\x10\x00\x12\x11\n\rTRACE_CONTEXT\x10\x01\x12\x12\n\x0eGRPC_TRACE_BIN\x10\x02\x12\x17\n\x13\x43LOUD_TRACE_CONTEXT\x10\x03\x12\x06\n\x02\x42\x33\x10\x04:-\x9a\xc5\x88\x1e(\n&envoy.config.trace.v2.OpenCensusConfigJ\x04\x08\x07\x10\x08\x42\xb9\x01\n#io.envoyproxy.envoy.config.trace.v3B\x0fOpencensusProtoP\x01ZDgithub.com/envoyproxy/go-control-plane/envoy/config/trace/v3;tracev3\xf2\x98\xfe\x8f\x05-\x12+envoy.extensions.tracers.opencensus.v4alpha\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_OPENCENSUSCONFIG = DESCRIPTOR.message_types_by_name['OpenCensusConfig']
_OPENCENSUSCONFIG_TRACECONTEXT = _OPENCENSUSCONFIG.enum_types_by_name['TraceContext']
OpenCensusConfig = _reflection.GeneratedProtocolMessageType('OpenCensusConfig', (_message.Message,), {
  'DESCRIPTOR' : _OPENCENSUSCONFIG,
  '__module__' : 'envoy.config.trace.v3.opencensus_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.trace.v3.OpenCensusConfig)
  })
_sym_db.RegisterMessage(OpenCensusConfig)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#io.envoyproxy.envoy.config.trace.v3B\017OpencensusProtoP\001ZDgithub.com/envoyproxy/go-control-plane/envoy/config/trace/v3;tracev3\362\230\376\217\005-\022+envoy.extensions.tracers.opencensus.v4alpha\272\200\310\321\006\002\020\002'
  _OPENCENSUSCONFIG.fields_by_name['zipkin_exporter_enabled']._options = None
  _OPENCENSUSCONFIG.fields_by_name['zipkin_exporter_enabled']._serialized_options = b'\030\001\222\307\206\330\004\0033.0'
  _OPENCENSUSCONFIG.fields_by_name['zipkin_url']._options = None
  _OPENCENSUSCONFIG.fields_by_name['zipkin_url']._serialized_options = b'\030\001\222\307\206\330\004\0033.0'
  _OPENCENSUSCONFIG._options = None
  _OPENCENSUSCONFIG._serialized_options = b'\232\305\210\036(\n&envoy.config.trace.v2.OpenCensusConfig'
  _OPENCENSUSCONFIG._serialized_start=288
  _OPENCENSUSCONFIG._serialized_end=1095
  _OPENCENSUSCONFIG_TRACECONTEXT._serialized_start=946
  _OPENCENSUSCONFIG_TRACECONTEXT._serialized_end=1042
# @@protoc_insertion_point(module_scope)
