# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rbt/cloud/v1alpha1/istio/envoy_filter_spec.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n0rbt/cloud/v1alpha1/istio/envoy_filter_spec.proto\x12\x19istio.networking.v1alpha3\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1fgoogle/api/field_behavior.proto\"\x9b\x17\n\x0b\x45nvoyFilter\x12\x46\n\x11workload_selector\x18\x03 \x01(\x0b\x32+.istio.networking.v1alpha3.WorkloadSelector\x12\x44\n\ntargetRefs\x18\x06 \x03(\x0b\x32\x30.istio.networking.v1alpha3.PolicyTargetReference\x12U\n\x0e\x63onfig_patches\x18\x04 \x03(\x0b\x32=.istio.networking.v1alpha3.EnvoyFilter.EnvoyConfigObjectPatch\x12\x10\n\x08priority\x18\x05 \x01(\x05\x1a\xa7\x01\n\nProxyMatch\x12\x15\n\rproxy_version\x18\x01 \x01(\t\x12Q\n\x08metadata\x18\x02 \x03(\x0b\x32?.istio.networking.v1alpha3.EnvoyFilter.ProxyMatch.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1aR\n\x0c\x43lusterMatch\x12\x13\n\x0bport_number\x18\x01 \x01(\r\x12\x0f\n\x07service\x18\x02 \x01(\t\x12\x0e\n\x06subset\x18\x03 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x1a\xfc\x03\n\x17RouteConfigurationMatch\x12\x13\n\x0bport_number\x18\x01 \x01(\r\x12\x11\n\tport_name\x18\x02 \x01(\t\x12\x0f\n\x07gateway\x18\x03 \x01(\t\x12^\n\x05vhost\x18\x04 \x01(\x0b\x32O.istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch.VirtualHostMatch\x12\x0c\n\x04name\x18\x05 \x01(\t\x1a\xbd\x01\n\nRouteMatch\x12\x0c\n\x04name\x18\x01 \x01(\t\x12`\n\x06\x61\x63tion\x18\x02 \x01(\x0e\x32P.istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch.RouteMatch.Action\"?\n\x06\x41\x63tion\x12\x07\n\x03\x41NY\x10\x00\x12\t\n\x05ROUTE\x10\x01\x12\x0c\n\x08REDIRECT\x10\x02\x12\x13\n\x0f\x44IRECT_RESPONSE\x10\x03\x1az\n\x10VirtualHostMatch\x12\x0c\n\x04name\x18\x01 \x01(\t\x12X\n\x05route\x18\x02 \x01(\x0b\x32I.istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch.RouteMatch\x1a\xa8\x04\n\rListenerMatch\x12\x13\n\x0bport_number\x18\x01 \x01(\r\x12\x11\n\tport_name\x18\x02 \x01(\t\x12[\n\x0c\x66ilter_chain\x18\x03 \x01(\x0b\x32\x45.istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.FilterChainMatch\x12\x17\n\x0flistener_filter\x18\x05 \x01(\t\x12\x0c\n\x04name\x18\x04 \x01(\t\x1a\xd4\x01\n\x10\x46ilterChainMatch\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0b\n\x03sni\x18\x02 \x01(\t\x12\x1a\n\x12transport_protocol\x18\x03 \x01(\t\x12\x1d\n\x15\x61pplication_protocols\x18\x04 \x01(\t\x12P\n\x06\x66ilter\x18\x05 \x01(\x0b\x32@.istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.FilterMatch\x12\x18\n\x10\x64\x65stination_port\x18\x06 \x01(\r\x1at\n\x0b\x46ilterMatch\x12\x0c\n\x04name\x18\x01 \x01(\t\x12W\n\nsub_filter\x18\x02 \x01(\x0b\x32\x43.istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.SubFilterMatch\x1a\x1e\n\x0eSubFilterMatch\x12\x0c\n\x04name\x18\x01 \x01(\t\x1a\x89\x03\n\x05Patch\x12I\n\toperation\x18\x01 \x01(\x0e\x32\x36.istio.networking.v1alpha3.EnvoyFilter.Patch.Operation\x12&\n\x05value\x18\x02 \x01(\x0b\x32\x17.google.protobuf.Struct\x12N\n\x0c\x66ilter_class\x18\x03 \x01(\x0e\x32\x38.istio.networking.v1alpha3.EnvoyFilter.Patch.FilterClass\"|\n\tOperation\x12\x0b\n\x07INVALID\x10\x00\x12\t\n\x05MERGE\x10\x01\x12\x07\n\x03\x41\x44\x44\x10\x02\x12\n\n\x06REMOVE\x10\x03\x12\x11\n\rINSERT_BEFORE\x10\x04\x12\x10\n\x0cINSERT_AFTER\x10\x05\x12\x10\n\x0cINSERT_FIRST\x10\x06\x12\x0b\n\x07REPLACE\x10\x07\"?\n\x0b\x46ilterClass\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\t\n\x05\x41UTHN\x10\x01\x12\t\n\x05\x41UTHZ\x10\x02\x12\t\n\x05STATS\x10\x03\x1a\xa1\x03\n\x16\x45nvoyConfigObjectMatch\x12\x44\n\x07\x63ontext\x18\x01 \x01(\x0e\x32\x33.istio.networking.v1alpha3.EnvoyFilter.PatchContext\x12@\n\x05proxy\x18\x02 \x01(\x0b\x32\x31.istio.networking.v1alpha3.EnvoyFilter.ProxyMatch\x12H\n\x08listener\x18\x03 \x01(\x0b\x32\x34.istio.networking.v1alpha3.EnvoyFilter.ListenerMatchH\x00\x12]\n\x13route_configuration\x18\x04 \x01(\x0b\x32>.istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatchH\x00\x12\x46\n\x07\x63luster\x18\x05 \x01(\x0b\x32\x33.istio.networking.v1alpha3.EnvoyFilter.ClusterMatchH\x00\x42\x0e\n\x0cobject_types\x1a\xe5\x01\n\x16\x45nvoyConfigObjectPatch\x12@\n\x08\x61pply_to\x18\x01 \x01(\x0e\x32..istio.networking.v1alpha3.EnvoyFilter.ApplyTo\x12L\n\x05match\x18\x02 \x01(\x0b\x32=.istio.networking.v1alpha3.EnvoyFilter.EnvoyConfigObjectMatch\x12;\n\x05patch\x18\x03 \x01(\x0b\x32,.istio.networking.v1alpha3.EnvoyFilter.Patch\"\xdd\x01\n\x07\x41pplyTo\x12\x0b\n\x07INVALID\x10\x00\x12\x0c\n\x08LISTENER\x10\x01\x12\x10\n\x0c\x46ILTER_CHAIN\x10\x02\x12\x12\n\x0eNETWORK_FILTER\x10\x03\x12\x0f\n\x0bHTTP_FILTER\x10\x04\x12\x17\n\x13ROUTE_CONFIGURATION\x10\x05\x12\x10\n\x0cVIRTUAL_HOST\x10\x06\x12\x0e\n\nHTTP_ROUTE\x10\x07\x12\x0b\n\x07\x43LUSTER\x10\x08\x12\x14\n\x10\x45XTENSION_CONFIG\x10\t\x12\r\n\tBOOTSTRAP\x10\n\x12\x13\n\x0fLISTENER_FILTER\x10\x0b\"O\n\x0cPatchContext\x12\x07\n\x03\x41NY\x10\x00\x12\x13\n\x0fSIDECAR_INBOUND\x10\x01\x12\x14\n\x10SIDECAR_OUTBOUND\x10\x02\x12\x0b\n\x07GATEWAY\x10\x03J\x04\x08\x01\x10\x02J\x04\x08\x02\x10\x03R\x07\x66iltersR\x0fworkload_labels\"\x8a\x01\n\x10WorkloadSelector\x12G\n\x06labels\x18\x01 \x03(\x0b\x32\x37.istio.networking.v1alpha3.WorkloadSelector.LabelsEntry\x1a-\n\x0bLabelsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"_\n\x15PolicyTargetReference\x12\r\n\x05group\x18\x01 \x01(\t\x12\x11\n\x04kind\x18\x02 \x01(\tB\x03\xe0\x41\x02\x12\x11\n\x04name\x18\x03 \x01(\tB\x03\xe0\x41\x02\x12\x11\n\tnamespace\x18\x04 \x01(\tB\"Z istio.io/api/networking/v1alpha3b\x06proto3')



_ENVOYFILTER = DESCRIPTOR.message_types_by_name['EnvoyFilter']
_ENVOYFILTER_PROXYMATCH = _ENVOYFILTER.nested_types_by_name['ProxyMatch']
_ENVOYFILTER_PROXYMATCH_METADATAENTRY = _ENVOYFILTER_PROXYMATCH.nested_types_by_name['MetadataEntry']
_ENVOYFILTER_CLUSTERMATCH = _ENVOYFILTER.nested_types_by_name['ClusterMatch']
_ENVOYFILTER_ROUTECONFIGURATIONMATCH = _ENVOYFILTER.nested_types_by_name['RouteConfigurationMatch']
_ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH = _ENVOYFILTER_ROUTECONFIGURATIONMATCH.nested_types_by_name['RouteMatch']
_ENVOYFILTER_ROUTECONFIGURATIONMATCH_VIRTUALHOSTMATCH = _ENVOYFILTER_ROUTECONFIGURATIONMATCH.nested_types_by_name['VirtualHostMatch']
_ENVOYFILTER_LISTENERMATCH = _ENVOYFILTER.nested_types_by_name['ListenerMatch']
_ENVOYFILTER_LISTENERMATCH_FILTERCHAINMATCH = _ENVOYFILTER_LISTENERMATCH.nested_types_by_name['FilterChainMatch']
_ENVOYFILTER_LISTENERMATCH_FILTERMATCH = _ENVOYFILTER_LISTENERMATCH.nested_types_by_name['FilterMatch']
_ENVOYFILTER_LISTENERMATCH_SUBFILTERMATCH = _ENVOYFILTER_LISTENERMATCH.nested_types_by_name['SubFilterMatch']
_ENVOYFILTER_PATCH = _ENVOYFILTER.nested_types_by_name['Patch']
_ENVOYFILTER_ENVOYCONFIGOBJECTMATCH = _ENVOYFILTER.nested_types_by_name['EnvoyConfigObjectMatch']
_ENVOYFILTER_ENVOYCONFIGOBJECTPATCH = _ENVOYFILTER.nested_types_by_name['EnvoyConfigObjectPatch']
_WORKLOADSELECTOR = DESCRIPTOR.message_types_by_name['WorkloadSelector']
_WORKLOADSELECTOR_LABELSENTRY = _WORKLOADSELECTOR.nested_types_by_name['LabelsEntry']
_POLICYTARGETREFERENCE = DESCRIPTOR.message_types_by_name['PolicyTargetReference']
_ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH_ACTION = _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH.enum_types_by_name['Action']
_ENVOYFILTER_PATCH_OPERATION = _ENVOYFILTER_PATCH.enum_types_by_name['Operation']
_ENVOYFILTER_PATCH_FILTERCLASS = _ENVOYFILTER_PATCH.enum_types_by_name['FilterClass']
_ENVOYFILTER_APPLYTO = _ENVOYFILTER.enum_types_by_name['ApplyTo']
_ENVOYFILTER_PATCHCONTEXT = _ENVOYFILTER.enum_types_by_name['PatchContext']
EnvoyFilter = _reflection.GeneratedProtocolMessageType('EnvoyFilter', (_message.Message,), {

  'ProxyMatch' : _reflection.GeneratedProtocolMessageType('ProxyMatch', (_message.Message,), {

    'MetadataEntry' : _reflection.GeneratedProtocolMessageType('MetadataEntry', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_PROXYMATCH_METADATAENTRY,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ProxyMatch.MetadataEntry)
      })
    ,
    'DESCRIPTOR' : _ENVOYFILTER_PROXYMATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ProxyMatch)
    })
  ,

  'ClusterMatch' : _reflection.GeneratedProtocolMessageType('ClusterMatch', (_message.Message,), {
    'DESCRIPTOR' : _ENVOYFILTER_CLUSTERMATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ClusterMatch)
    })
  ,

  'RouteConfigurationMatch' : _reflection.GeneratedProtocolMessageType('RouteConfigurationMatch', (_message.Message,), {

    'RouteMatch' : _reflection.GeneratedProtocolMessageType('RouteMatch', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch.RouteMatch)
      })
    ,

    'VirtualHostMatch' : _reflection.GeneratedProtocolMessageType('VirtualHostMatch', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_ROUTECONFIGURATIONMATCH_VIRTUALHOSTMATCH,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch.VirtualHostMatch)
      })
    ,
    'DESCRIPTOR' : _ENVOYFILTER_ROUTECONFIGURATIONMATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.RouteConfigurationMatch)
    })
  ,

  'ListenerMatch' : _reflection.GeneratedProtocolMessageType('ListenerMatch', (_message.Message,), {

    'FilterChainMatch' : _reflection.GeneratedProtocolMessageType('FilterChainMatch', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_LISTENERMATCH_FILTERCHAINMATCH,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.FilterChainMatch)
      })
    ,

    'FilterMatch' : _reflection.GeneratedProtocolMessageType('FilterMatch', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_LISTENERMATCH_FILTERMATCH,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.FilterMatch)
      })
    ,

    'SubFilterMatch' : _reflection.GeneratedProtocolMessageType('SubFilterMatch', (_message.Message,), {
      'DESCRIPTOR' : _ENVOYFILTER_LISTENERMATCH_SUBFILTERMATCH,
      '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
      # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ListenerMatch.SubFilterMatch)
      })
    ,
    'DESCRIPTOR' : _ENVOYFILTER_LISTENERMATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.ListenerMatch)
    })
  ,

  'Patch' : _reflection.GeneratedProtocolMessageType('Patch', (_message.Message,), {
    'DESCRIPTOR' : _ENVOYFILTER_PATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.Patch)
    })
  ,

  'EnvoyConfigObjectMatch' : _reflection.GeneratedProtocolMessageType('EnvoyConfigObjectMatch', (_message.Message,), {
    'DESCRIPTOR' : _ENVOYFILTER_ENVOYCONFIGOBJECTMATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.EnvoyConfigObjectMatch)
    })
  ,

  'EnvoyConfigObjectPatch' : _reflection.GeneratedProtocolMessageType('EnvoyConfigObjectPatch', (_message.Message,), {
    'DESCRIPTOR' : _ENVOYFILTER_ENVOYCONFIGOBJECTPATCH,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter.EnvoyConfigObjectPatch)
    })
  ,
  'DESCRIPTOR' : _ENVOYFILTER,
  '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
  # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.EnvoyFilter)
  })
_sym_db.RegisterMessage(EnvoyFilter)
_sym_db.RegisterMessage(EnvoyFilter.ProxyMatch)
_sym_db.RegisterMessage(EnvoyFilter.ProxyMatch.MetadataEntry)
_sym_db.RegisterMessage(EnvoyFilter.ClusterMatch)
_sym_db.RegisterMessage(EnvoyFilter.RouteConfigurationMatch)
_sym_db.RegisterMessage(EnvoyFilter.RouteConfigurationMatch.RouteMatch)
_sym_db.RegisterMessage(EnvoyFilter.RouteConfigurationMatch.VirtualHostMatch)
_sym_db.RegisterMessage(EnvoyFilter.ListenerMatch)
_sym_db.RegisterMessage(EnvoyFilter.ListenerMatch.FilterChainMatch)
_sym_db.RegisterMessage(EnvoyFilter.ListenerMatch.FilterMatch)
_sym_db.RegisterMessage(EnvoyFilter.ListenerMatch.SubFilterMatch)
_sym_db.RegisterMessage(EnvoyFilter.Patch)
_sym_db.RegisterMessage(EnvoyFilter.EnvoyConfigObjectMatch)
_sym_db.RegisterMessage(EnvoyFilter.EnvoyConfigObjectPatch)

WorkloadSelector = _reflection.GeneratedProtocolMessageType('WorkloadSelector', (_message.Message,), {

  'LabelsEntry' : _reflection.GeneratedProtocolMessageType('LabelsEntry', (_message.Message,), {
    'DESCRIPTOR' : _WORKLOADSELECTOR_LABELSENTRY,
    '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
    # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.WorkloadSelector.LabelsEntry)
    })
  ,
  'DESCRIPTOR' : _WORKLOADSELECTOR,
  '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
  # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.WorkloadSelector)
  })
_sym_db.RegisterMessage(WorkloadSelector)
_sym_db.RegisterMessage(WorkloadSelector.LabelsEntry)

PolicyTargetReference = _reflection.GeneratedProtocolMessageType('PolicyTargetReference', (_message.Message,), {
  'DESCRIPTOR' : _POLICYTARGETREFERENCE,
  '__module__' : 'rbt.cloud.v1alpha1.istio.envoy_filter_spec_pb2'
  # @@protoc_insertion_point(class_scope:istio.networking.v1alpha3.PolicyTargetReference)
  })
_sym_db.RegisterMessage(PolicyTargetReference)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z istio.io/api/networking/v1alpha3'
  _ENVOYFILTER_PROXYMATCH_METADATAENTRY._options = None
  _ENVOYFILTER_PROXYMATCH_METADATAENTRY._serialized_options = b'8\001'
  _WORKLOADSELECTOR_LABELSENTRY._options = None
  _WORKLOADSELECTOR_LABELSENTRY._serialized_options = b'8\001'
  _POLICYTARGETREFERENCE.fields_by_name['kind']._options = None
  _POLICYTARGETREFERENCE.fields_by_name['kind']._serialized_options = b'\340A\002'
  _POLICYTARGETREFERENCE.fields_by_name['name']._options = None
  _POLICYTARGETREFERENCE.fields_by_name['name']._serialized_options = b'\340A\002'
  _ENVOYFILTER._serialized_start=143
  _ENVOYFILTER._serialized_end=3114
  _ENVOYFILTER_PROXYMATCH._serialized_start=406
  _ENVOYFILTER_PROXYMATCH._serialized_end=573
  _ENVOYFILTER_PROXYMATCH_METADATAENTRY._serialized_start=526
  _ENVOYFILTER_PROXYMATCH_METADATAENTRY._serialized_end=573
  _ENVOYFILTER_CLUSTERMATCH._serialized_start=575
  _ENVOYFILTER_CLUSTERMATCH._serialized_end=657
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH._serialized_start=660
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH._serialized_end=1168
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH._serialized_start=855
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH._serialized_end=1044
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH_ACTION._serialized_start=981
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_ROUTEMATCH_ACTION._serialized_end=1044
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_VIRTUALHOSTMATCH._serialized_start=1046
  _ENVOYFILTER_ROUTECONFIGURATIONMATCH_VIRTUALHOSTMATCH._serialized_end=1168
  _ENVOYFILTER_LISTENERMATCH._serialized_start=1171
  _ENVOYFILTER_LISTENERMATCH._serialized_end=1723
  _ENVOYFILTER_LISTENERMATCH_FILTERCHAINMATCH._serialized_start=1361
  _ENVOYFILTER_LISTENERMATCH_FILTERCHAINMATCH._serialized_end=1573
  _ENVOYFILTER_LISTENERMATCH_FILTERMATCH._serialized_start=1575
  _ENVOYFILTER_LISTENERMATCH_FILTERMATCH._serialized_end=1691
  _ENVOYFILTER_LISTENERMATCH_SUBFILTERMATCH._serialized_start=1693
  _ENVOYFILTER_LISTENERMATCH_SUBFILTERMATCH._serialized_end=1723
  _ENVOYFILTER_PATCH._serialized_start=1726
  _ENVOYFILTER_PATCH._serialized_end=2119
  _ENVOYFILTER_PATCH_OPERATION._serialized_start=1930
  _ENVOYFILTER_PATCH_OPERATION._serialized_end=2054
  _ENVOYFILTER_PATCH_FILTERCLASS._serialized_start=2056
  _ENVOYFILTER_PATCH_FILTERCLASS._serialized_end=2119
  _ENVOYFILTER_ENVOYCONFIGOBJECTMATCH._serialized_start=2122
  _ENVOYFILTER_ENVOYCONFIGOBJECTMATCH._serialized_end=2539
  _ENVOYFILTER_ENVOYCONFIGOBJECTPATCH._serialized_start=2542
  _ENVOYFILTER_ENVOYCONFIGOBJECTPATCH._serialized_end=2771
  _ENVOYFILTER_APPLYTO._serialized_start=2774
  _ENVOYFILTER_APPLYTO._serialized_end=2995
  _ENVOYFILTER_PATCHCONTEXT._serialized_start=2997
  _ENVOYFILTER_PATCHCONTEXT._serialized_end=3076
  _WORKLOADSELECTOR._serialized_start=3117
  _WORKLOADSELECTOR._serialized_end=3255
  _WORKLOADSELECTOR_LABELSENTRY._serialized_start=3210
  _WORKLOADSELECTOR_LABELSENTRY._serialized_end=3255
  _POLICYTARGETREFERENCE._serialized_start=3257
  _POLICYTARGETREFERENCE._serialized_end=3352
# @@protoc_insertion_point(module_scope)
