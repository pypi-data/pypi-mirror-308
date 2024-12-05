# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/config/endpoint/v3/load_report.proto
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
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n*envoy/config/endpoint/v3/load_report.proto\x12\x18\x65nvoy.config.endpoint.v3\x1a\"envoy/config/core/v3/address.proto\x1a\x1f\x65nvoy/config/core/v3/base.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\x1a\x17validate/validate.proto\"\xb3\x03\n\x15UpstreamLocalityStats\x12\x30\n\x08locality\x18\x01 \x01(\x0b\x32\x1e.envoy.config.core.v3.Locality\x12!\n\x19total_successful_requests\x18\x02 \x01(\x04\x12\"\n\x1atotal_requests_in_progress\x18\x03 \x01(\x04\x12\x1c\n\x14total_error_requests\x18\x04 \x01(\x04\x12\x1d\n\x15total_issued_requests\x18\x08 \x01(\x04\x12L\n\x11load_metric_stats\x18\x05 \x03(\x0b\x32\x31.envoy.config.endpoint.v3.EndpointLoadMetricStats\x12P\n\x17upstream_endpoint_stats\x18\x07 \x03(\x0b\x32/.envoy.config.endpoint.v3.UpstreamEndpointStats\x12\x10\n\x08priority\x18\x06 \x01(\r:2\x9a\xc5\x88\x1e-\n+envoy.api.v2.endpoint.UpstreamLocalityStats\"\xf8\x02\n\x15UpstreamEndpointStats\x12.\n\x07\x61\x64\x64ress\x18\x01 \x01(\x0b\x32\x1d.envoy.config.core.v3.Address\x12)\n\x08metadata\x18\x06 \x01(\x0b\x32\x17.google.protobuf.Struct\x12!\n\x19total_successful_requests\x18\x02 \x01(\x04\x12\"\n\x1atotal_requests_in_progress\x18\x03 \x01(\x04\x12\x1c\n\x14total_error_requests\x18\x04 \x01(\x04\x12\x1d\n\x15total_issued_requests\x18\x07 \x01(\x04\x12L\n\x11load_metric_stats\x18\x05 \x03(\x0b\x32\x31.envoy.config.endpoint.v3.EndpointLoadMetricStats:2\x9a\xc5\x88\x1e-\n+envoy.api.v2.endpoint.UpstreamEndpointStats\"\xab\x01\n\x17\x45ndpointLoadMetricStats\x12\x13\n\x0bmetric_name\x18\x01 \x01(\t\x12)\n!num_requests_finished_with_metric\x18\x02 \x01(\x04\x12\x1a\n\x12total_metric_value\x18\x03 \x01(\x01:4\x9a\xc5\x88\x1e/\n-envoy.api.v2.endpoint.EndpointLoadMetricStats\"\xfd\x03\n\x0c\x43lusterStats\x12\x1d\n\x0c\x63luster_name\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12\x1c\n\x14\x63luster_service_name\x18\x06 \x01(\t\x12Z\n\x17upstream_locality_stats\x18\x02 \x03(\x0b\x32/.envoy.config.endpoint.v3.UpstreamLocalityStatsB\x08\xfa\x42\x05\x92\x01\x02\x08\x01\x12\x1e\n\x16total_dropped_requests\x18\x03 \x01(\x04\x12P\n\x10\x64ropped_requests\x18\x05 \x03(\x0b\x32\x36.envoy.config.endpoint.v3.ClusterStats.DroppedRequests\x12\x37\n\x14load_report_interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x1a~\n\x0f\x44roppedRequests\x12\x19\n\x08\x63\x61tegory\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12\x15\n\rdropped_count\x18\x02 \x01(\x04:9\x9a\xc5\x88\x1e\x34\n2envoy.api.v2.endpoint.ClusterStats.DroppedRequests:)\x9a\xc5\x88\x1e$\n\"envoy.api.v2.endpoint.ClusterStatsB\x8f\x01\n&io.envoyproxy.envoy.config.endpoint.v3B\x0fLoadReportProtoP\x01ZJgithub.com/envoyproxy/go-control-plane/envoy/config/endpoint/v3;endpointv3\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_UPSTREAMLOCALITYSTATS = DESCRIPTOR.message_types_by_name['UpstreamLocalityStats']
_UPSTREAMENDPOINTSTATS = DESCRIPTOR.message_types_by_name['UpstreamEndpointStats']
_ENDPOINTLOADMETRICSTATS = DESCRIPTOR.message_types_by_name['EndpointLoadMetricStats']
_CLUSTERSTATS = DESCRIPTOR.message_types_by_name['ClusterStats']
_CLUSTERSTATS_DROPPEDREQUESTS = _CLUSTERSTATS.nested_types_by_name['DroppedRequests']
UpstreamLocalityStats = _reflection.GeneratedProtocolMessageType('UpstreamLocalityStats', (_message.Message,), {
  'DESCRIPTOR' : _UPSTREAMLOCALITYSTATS,
  '__module__' : 'envoy.config.endpoint.v3.load_report_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.endpoint.v3.UpstreamLocalityStats)
  })
_sym_db.RegisterMessage(UpstreamLocalityStats)

UpstreamEndpointStats = _reflection.GeneratedProtocolMessageType('UpstreamEndpointStats', (_message.Message,), {
  'DESCRIPTOR' : _UPSTREAMENDPOINTSTATS,
  '__module__' : 'envoy.config.endpoint.v3.load_report_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.endpoint.v3.UpstreamEndpointStats)
  })
_sym_db.RegisterMessage(UpstreamEndpointStats)

EndpointLoadMetricStats = _reflection.GeneratedProtocolMessageType('EndpointLoadMetricStats', (_message.Message,), {
  'DESCRIPTOR' : _ENDPOINTLOADMETRICSTATS,
  '__module__' : 'envoy.config.endpoint.v3.load_report_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.endpoint.v3.EndpointLoadMetricStats)
  })
_sym_db.RegisterMessage(EndpointLoadMetricStats)

ClusterStats = _reflection.GeneratedProtocolMessageType('ClusterStats', (_message.Message,), {

  'DroppedRequests' : _reflection.GeneratedProtocolMessageType('DroppedRequests', (_message.Message,), {
    'DESCRIPTOR' : _CLUSTERSTATS_DROPPEDREQUESTS,
    '__module__' : 'envoy.config.endpoint.v3.load_report_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.endpoint.v3.ClusterStats.DroppedRequests)
    })
  ,
  'DESCRIPTOR' : _CLUSTERSTATS,
  '__module__' : 'envoy.config.endpoint.v3.load_report_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.endpoint.v3.ClusterStats)
  })
_sym_db.RegisterMessage(ClusterStats)
_sym_db.RegisterMessage(ClusterStats.DroppedRequests)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n&io.envoyproxy.envoy.config.endpoint.v3B\017LoadReportProtoP\001ZJgithub.com/envoyproxy/go-control-plane/envoy/config/endpoint/v3;endpointv3\272\200\310\321\006\002\020\002'
  _UPSTREAMLOCALITYSTATS._options = None
  _UPSTREAMLOCALITYSTATS._serialized_options = b'\232\305\210\036-\n+envoy.api.v2.endpoint.UpstreamLocalityStats'
  _UPSTREAMENDPOINTSTATS._options = None
  _UPSTREAMENDPOINTSTATS._serialized_options = b'\232\305\210\036-\n+envoy.api.v2.endpoint.UpstreamEndpointStats'
  _ENDPOINTLOADMETRICSTATS._options = None
  _ENDPOINTLOADMETRICSTATS._serialized_options = b'\232\305\210\036/\n-envoy.api.v2.endpoint.EndpointLoadMetricStats'
  _CLUSTERSTATS_DROPPEDREQUESTS.fields_by_name['category']._options = None
  _CLUSTERSTATS_DROPPEDREQUESTS.fields_by_name['category']._serialized_options = b'\372B\004r\002\020\001'
  _CLUSTERSTATS_DROPPEDREQUESTS._options = None
  _CLUSTERSTATS_DROPPEDREQUESTS._serialized_options = b'\232\305\210\0364\n2envoy.api.v2.endpoint.ClusterStats.DroppedRequests'
  _CLUSTERSTATS.fields_by_name['cluster_name']._options = None
  _CLUSTERSTATS.fields_by_name['cluster_name']._serialized_options = b'\372B\004r\002\020\001'
  _CLUSTERSTATS.fields_by_name['upstream_locality_stats']._options = None
  _CLUSTERSTATS.fields_by_name['upstream_locality_stats']._serialized_options = b'\372B\005\222\001\002\010\001'
  _CLUSTERSTATS._options = None
  _CLUSTERSTATS._serialized_options = b'\232\305\210\036$\n\"envoy.api.v2.endpoint.ClusterStats'
  _UPSTREAMLOCALITYSTATS._serialized_start=295
  _UPSTREAMLOCALITYSTATS._serialized_end=730
  _UPSTREAMENDPOINTSTATS._serialized_start=733
  _UPSTREAMENDPOINTSTATS._serialized_end=1109
  _ENDPOINTLOADMETRICSTATS._serialized_start=1112
  _ENDPOINTLOADMETRICSTATS._serialized_end=1283
  _CLUSTERSTATS._serialized_start=1286
  _CLUSTERSTATS._serialized_end=1795
  _CLUSTERSTATS_DROPPEDREQUESTS._serialized_start=1626
  _CLUSTERSTATS_DROPPEDREQUESTS._serialized_end=1752
# @@protoc_insertion_point(module_scope)
