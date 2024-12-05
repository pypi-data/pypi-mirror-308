# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/config/core/v3/protocol.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from envoy.config.core.v3 import extension_pb2 as envoy_dot_config_dot_core_dot_v3_dot_extension__pb2
from envoy.type.v3 import percent_pb2 as envoy_dot_type_dot_v3_dot_percent__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from xds.annotations.v3 import status_pb2 as xds_dot_annotations_dot_v3_dot_status__pb2
from envoy.annotations import deprecation_pb2 as envoy_dot_annotations_dot_deprecation__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n#envoy/config/core/v3/protocol.proto\x12\x14\x65nvoy.config.core.v3\x1a$envoy/config/core/v3/extension.proto\x1a\x1b\x65nvoy/type/v3/percent.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1fxds/annotations/v3/status.proto\x1a#envoy/annotations/deprecation.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\x1a\x17validate/validate.proto\"A\n\x12TcpProtocolOptions:+\x9a\xc5\x88\x1e&\n$envoy.api.v2.core.TcpProtocolOptions\"\x99\x01\n\x15QuicKeepAliveSettings\x12=\n\x0cmax_interval\x18\x01 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0c\xfa\x42\t\xaa\x01\x06\"\x00\x32\x02\x08\x01\x12\x41\n\x10initial_interval\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0c\xfa\x42\t\xaa\x01\x06\"\x00\x32\x02\x08\x01\"\xa4\x03\n\x13QuicProtocolOptions\x12\x45\n\x16max_concurrent_streams\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02(\x01\x12N\n\x1ainitial_stream_window_size\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x0c\xfa\x42\t*\x07\x18\x80\x80\x80\x08(\x01\x12R\n\x1einitial_connection_window_size\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x0c\xfa\x42\t*\x07\x18\x80\x80\x80\x0c(\x01\x12W\n&num_timeouts_to_trigger_port_migration\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\t\xfa\x42\x06*\x04\x18\x05(\x00\x12I\n\x14\x63onnection_keepalive\x18\x05 \x01(\x0b\x32+.envoy.config.core.v3.QuicKeepAliveSettings\"\xb1\x01\n\x1bUpstreamHttpProtocolOptions\x12\x10\n\x08\x61uto_sni\x18\x01 \x01(\x08\x12\x1b\n\x13\x61uto_san_validation\x18\x02 \x01(\x08\x12-\n\x18override_auto_sni_header\x18\x03 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xd0\x01\x01:4\x9a\xc5\x88\x1e/\n-envoy.api.v2.core.UpstreamHttpProtocolOptions\"\xa6\x03\n\x1e\x41lternateProtocolsCacheOptions\x12\x15\n\x04name\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x12:\n\x0bmax_entries\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02 \x00\x12J\n\x16key_value_store_config\x18\x03 \x01(\x0b\x32*.envoy.config.core.v3.TypedExtensionConfig\x12o\n\x14prepopulated_entries\x18\x04 \x03(\x0b\x32Q.envoy.config.core.v3.AlternateProtocolsCacheOptions.AlternateProtocolsCacheEntry\x12\x1a\n\x12\x63\x61nonical_suffixes\x18\x05 \x03(\t\x1aX\n\x1c\x41lternateProtocolsCacheEntry\x12\x1d\n\x08hostname\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xd0\x01\x01\x12\x19\n\x04port\x18\x02 \x01(\rB\x0b\xfa\x42\x08*\x06\x10\xff\xff\x03 \x00\"\xae\x04\n\x13HttpProtocolOptions\x12/\n\x0cidle_timeout\x18\x01 \x01(\x0b\x32\x19.google.protobuf.Duration\x12:\n\x17max_connection_duration\x18\x03 \x01(\x0b\x32\x19.google.protobuf.Duration\x12@\n\x11max_headers_count\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02(\x01\x12\x36\n\x13max_stream_duration\x18\x04 \x01(\x0b\x32\x19.google.protobuf.Duration\x12o\n\x1fheaders_with_underscores_action\x18\x05 \x01(\x0e\x32\x46.envoy.config.core.v3.HttpProtocolOptions.HeadersWithUnderscoresAction\x12\x41\n\x1bmax_requests_per_connection\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\"N\n\x1cHeadersWithUnderscoresAction\x12\t\n\x05\x41LLOW\x10\x00\x12\x12\n\x0eREJECT_REQUEST\x10\x01\x12\x0f\n\x0b\x44ROP_HEADER\x10\x02:,\x9a\xc5\x88\x1e\'\n%envoy.api.v2.core.HttpProtocolOptions\"\xb8\x06\n\x14Http1ProtocolOptions\x12\x36\n\x12\x61llow_absolute_url\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x16\n\x0e\x61\x63\x63\x65pt_http_10\x18\x02 \x01(\x08\x12 \n\x18\x64\x65\x66\x61ult_host_for_http_10\x18\x03 \x01(\t\x12U\n\x11header_key_format\x18\x04 \x01(\x0b\x32:.envoy.config.core.v3.Http1ProtocolOptions.HeaderKeyFormat\x12\x17\n\x0f\x65nable_trailers\x18\x05 \x01(\x08\x12\x1c\n\x14\x61llow_chunked_length\x18\x06 \x01(\x08\x12Q\n-override_stream_error_on_invalid_http_message\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12 \n\x18send_fully_qualified_url\x18\x08 \x01(\x08\x1a\xfb\x02\n\x0fHeaderKeyFormat\x12g\n\x11proper_case_words\x18\x01 \x01(\x0b\x32J.envoy.config.core.v3.Http1ProtocolOptions.HeaderKeyFormat.ProperCaseWordsH\x00\x12H\n\x12stateful_formatter\x18\x08 \x01(\x0b\x32*.envoy.config.core.v3.TypedExtensionConfigH\x00\x1a`\n\x0fProperCaseWords:M\x9a\xc5\x88\x1eH\nFenvoy.api.v2.core.Http1ProtocolOptions.HeaderKeyFormat.ProperCaseWords:=\x9a\xc5\x88\x1e\x38\n6envoy.api.v2.core.Http1ProtocolOptions.HeaderKeyFormatB\x14\n\rheader_format\x12\x03\xf8\x42\x01:-\x9a\xc5\x88\x1e(\n&envoy.api.v2.core.Http1ProtocolOptions\"\x86\x02\n\x11KeepaliveSettings\x12\x39\n\x08interval\x18\x01 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0c\xfa\x42\t\xaa\x01\x06\x32\x04\x10\xc0\x84=\x12:\n\x07timeout\x18\x02 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0e\xfa\x42\x0b\xaa\x01\x08\x08\x01\x32\x04\x10\xc0\x84=\x12/\n\x0finterval_jitter\x18\x03 \x01(\x0b\x32\x16.envoy.type.v3.Percent\x12I\n\x18\x63onnection_idle_interval\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationB\x0c\xfa\x42\t\xaa\x01\x06\x32\x04\x10\xc0\x84=\"\xcd\n\n\x14Http2ProtocolOptions\x12\x36\n\x10hpack_table_size\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12K\n\x16max_concurrent_streams\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\r\xfa\x42\n*\x08\x18\xff\xff\xff\xff\x07(\x01\x12Q\n\x1ainitial_stream_window_size\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x0f\xfa\x42\x0c*\n\x18\xff\xff\xff\xff\x07(\xff\xff\x03\x12U\n\x1einitial_connection_window_size\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x0f\xfa\x42\x0c*\n\x18\xff\xff\xff\xff\x07(\xff\xff\x03\x12\x15\n\rallow_connect\x18\x05 \x01(\x08\x12\x16\n\x0e\x61llow_metadata\x18\x06 \x01(\x08\x12\x42\n\x13max_outbound_frames\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02(\x01\x12J\n\x1bmax_outbound_control_frames\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02(\x01\x12W\n1max_consecutive_inbound_frames_with_empty_payload\x18\t \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12L\n&max_inbound_priority_frames_per_stream\x18\n \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x12\x63\n4max_inbound_window_update_frames_per_data_frame_sent\x18\x0b \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x07\xfa\x42\x04*\x02(\x01\x12;\n&stream_error_on_invalid_http_messaging\x18\x0c \x01(\x08\x42\x0b\x18\x01\x92\xc7\x86\xd8\x04\x03\x33.0\x12Q\n-override_stream_error_on_invalid_http_message\x18\x0e \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12`\n\x1a\x63ustom_settings_parameters\x18\r \x03(\x0b\x32<.envoy.config.core.v3.Http2ProtocolOptions.SettingsParameter\x12\x45\n\x14\x63onnection_keepalive\x18\x0f \x01(\x0b\x32\'.envoy.config.core.v3.KeepaliveSettings\x1a\xd2\x01\n\x11SettingsParameter\x12\x45\n\nidentifier\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x13\xfa\x42\x08*\x06\x18\xff\xff\x03(\x00\xfa\x42\x05\x8a\x01\x02\x10\x01\x12\x35\n\x05value\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.UInt32ValueB\x08\xfa\x42\x05\x8a\x01\x02\x10\x01:?\x9a\xc5\x88\x1e:\n8envoy.api.v2.core.Http2ProtocolOptions.SettingsParameter:-\x9a\xc5\x88\x1e(\n&envoy.api.v2.core.Http2ProtocolOptions\"\x8f\x01\n\x13GrpcProtocolOptions\x12J\n\x16http2_protocol_options\x18\x01 \x01(\x0b\x32*.envoy.config.core.v3.Http2ProtocolOptions:,\x9a\xc5\x88\x1e\'\n%envoy.api.v2.core.GrpcProtocolOptions\"\xdd\x01\n\x14Http3ProtocolOptions\x12H\n\x15quic_protocol_options\x18\x01 \x01(\x0b\x32).envoy.config.core.v3.QuicProtocolOptions\x12Q\n-override_stream_error_on_invalid_http_message\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12(\n\x16\x61llow_extended_connect\x18\x05 \x01(\x08\x42\x08\xd2\xc6\xa4\xe1\x06\x02\x08\x01\"a\n\x1aSchemeHeaderTransformation\x12\x31\n\x13scheme_to_overwrite\x18\x01 \x01(\tB\x12\xfa\x42\x0fr\rR\x04httpR\x05httpsH\x00\x42\x10\n\x0etransformationB\x81\x01\n\"io.envoyproxy.envoy.config.core.v3B\rProtocolProtoP\x01ZBgithub.com/envoyproxy/go-control-plane/envoy/config/core/v3;corev3\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_TCPPROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['TcpProtocolOptions']
_QUICKEEPALIVESETTINGS = DESCRIPTOR.message_types_by_name['QuicKeepAliveSettings']
_QUICPROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['QuicProtocolOptions']
_UPSTREAMHTTPPROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['UpstreamHttpProtocolOptions']
_ALTERNATEPROTOCOLSCACHEOPTIONS = DESCRIPTOR.message_types_by_name['AlternateProtocolsCacheOptions']
_ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY = _ALTERNATEPROTOCOLSCACHEOPTIONS.nested_types_by_name['AlternateProtocolsCacheEntry']
_HTTPPROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['HttpProtocolOptions']
_HTTP1PROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['Http1ProtocolOptions']
_HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT = _HTTP1PROTOCOLOPTIONS.nested_types_by_name['HeaderKeyFormat']
_HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS = _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT.nested_types_by_name['ProperCaseWords']
_KEEPALIVESETTINGS = DESCRIPTOR.message_types_by_name['KeepaliveSettings']
_HTTP2PROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['Http2ProtocolOptions']
_HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER = _HTTP2PROTOCOLOPTIONS.nested_types_by_name['SettingsParameter']
_GRPCPROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['GrpcProtocolOptions']
_HTTP3PROTOCOLOPTIONS = DESCRIPTOR.message_types_by_name['Http3ProtocolOptions']
_SCHEMEHEADERTRANSFORMATION = DESCRIPTOR.message_types_by_name['SchemeHeaderTransformation']
_HTTPPROTOCOLOPTIONS_HEADERSWITHUNDERSCORESACTION = _HTTPPROTOCOLOPTIONS.enum_types_by_name['HeadersWithUnderscoresAction']
TcpProtocolOptions = _reflection.GeneratedProtocolMessageType('TcpProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _TCPPROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.TcpProtocolOptions)
  })
_sym_db.RegisterMessage(TcpProtocolOptions)

QuicKeepAliveSettings = _reflection.GeneratedProtocolMessageType('QuicKeepAliveSettings', (_message.Message,), {
  'DESCRIPTOR' : _QUICKEEPALIVESETTINGS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.QuicKeepAliveSettings)
  })
_sym_db.RegisterMessage(QuicKeepAliveSettings)

QuicProtocolOptions = _reflection.GeneratedProtocolMessageType('QuicProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _QUICPROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.QuicProtocolOptions)
  })
_sym_db.RegisterMessage(QuicProtocolOptions)

UpstreamHttpProtocolOptions = _reflection.GeneratedProtocolMessageType('UpstreamHttpProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _UPSTREAMHTTPPROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.UpstreamHttpProtocolOptions)
  })
_sym_db.RegisterMessage(UpstreamHttpProtocolOptions)

AlternateProtocolsCacheOptions = _reflection.GeneratedProtocolMessageType('AlternateProtocolsCacheOptions', (_message.Message,), {

  'AlternateProtocolsCacheEntry' : _reflection.GeneratedProtocolMessageType('AlternateProtocolsCacheEntry', (_message.Message,), {
    'DESCRIPTOR' : _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY,
    '__module__' : 'envoy.config.core.v3.protocol_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.core.v3.AlternateProtocolsCacheOptions.AlternateProtocolsCacheEntry)
    })
  ,
  'DESCRIPTOR' : _ALTERNATEPROTOCOLSCACHEOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.AlternateProtocolsCacheOptions)
  })
_sym_db.RegisterMessage(AlternateProtocolsCacheOptions)
_sym_db.RegisterMessage(AlternateProtocolsCacheOptions.AlternateProtocolsCacheEntry)

HttpProtocolOptions = _reflection.GeneratedProtocolMessageType('HttpProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _HTTPPROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.HttpProtocolOptions)
  })
_sym_db.RegisterMessage(HttpProtocolOptions)

Http1ProtocolOptions = _reflection.GeneratedProtocolMessageType('Http1ProtocolOptions', (_message.Message,), {

  'HeaderKeyFormat' : _reflection.GeneratedProtocolMessageType('HeaderKeyFormat', (_message.Message,), {

    'ProperCaseWords' : _reflection.GeneratedProtocolMessageType('ProperCaseWords', (_message.Message,), {
      'DESCRIPTOR' : _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS,
      '__module__' : 'envoy.config.core.v3.protocol_pb2'
      # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http1ProtocolOptions.HeaderKeyFormat.ProperCaseWords)
      })
    ,
    'DESCRIPTOR' : _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT,
    '__module__' : 'envoy.config.core.v3.protocol_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http1ProtocolOptions.HeaderKeyFormat)
    })
  ,
  'DESCRIPTOR' : _HTTP1PROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http1ProtocolOptions)
  })
_sym_db.RegisterMessage(Http1ProtocolOptions)
_sym_db.RegisterMessage(Http1ProtocolOptions.HeaderKeyFormat)
_sym_db.RegisterMessage(Http1ProtocolOptions.HeaderKeyFormat.ProperCaseWords)

KeepaliveSettings = _reflection.GeneratedProtocolMessageType('KeepaliveSettings', (_message.Message,), {
  'DESCRIPTOR' : _KEEPALIVESETTINGS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.KeepaliveSettings)
  })
_sym_db.RegisterMessage(KeepaliveSettings)

Http2ProtocolOptions = _reflection.GeneratedProtocolMessageType('Http2ProtocolOptions', (_message.Message,), {

  'SettingsParameter' : _reflection.GeneratedProtocolMessageType('SettingsParameter', (_message.Message,), {
    'DESCRIPTOR' : _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER,
    '__module__' : 'envoy.config.core.v3.protocol_pb2'
    # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http2ProtocolOptions.SettingsParameter)
    })
  ,
  'DESCRIPTOR' : _HTTP2PROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http2ProtocolOptions)
  })
_sym_db.RegisterMessage(Http2ProtocolOptions)
_sym_db.RegisterMessage(Http2ProtocolOptions.SettingsParameter)

GrpcProtocolOptions = _reflection.GeneratedProtocolMessageType('GrpcProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _GRPCPROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.GrpcProtocolOptions)
  })
_sym_db.RegisterMessage(GrpcProtocolOptions)

Http3ProtocolOptions = _reflection.GeneratedProtocolMessageType('Http3ProtocolOptions', (_message.Message,), {
  'DESCRIPTOR' : _HTTP3PROTOCOLOPTIONS,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.Http3ProtocolOptions)
  })
_sym_db.RegisterMessage(Http3ProtocolOptions)

SchemeHeaderTransformation = _reflection.GeneratedProtocolMessageType('SchemeHeaderTransformation', (_message.Message,), {
  'DESCRIPTOR' : _SCHEMEHEADERTRANSFORMATION,
  '__module__' : 'envoy.config.core.v3.protocol_pb2'
  # @@protoc_insertion_point(class_scope:envoy.config.core.v3.SchemeHeaderTransformation)
  })
_sym_db.RegisterMessage(SchemeHeaderTransformation)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\"io.envoyproxy.envoy.config.core.v3B\rProtocolProtoP\001ZBgithub.com/envoyproxy/go-control-plane/envoy/config/core/v3;corev3\272\200\310\321\006\002\020\002'
  _TCPPROTOCOLOPTIONS._options = None
  _TCPPROTOCOLOPTIONS._serialized_options = b'\232\305\210\036&\n$envoy.api.v2.core.TcpProtocolOptions'
  _QUICKEEPALIVESETTINGS.fields_by_name['max_interval']._options = None
  _QUICKEEPALIVESETTINGS.fields_by_name['max_interval']._serialized_options = b'\372B\t\252\001\006\"\0002\002\010\001'
  _QUICKEEPALIVESETTINGS.fields_by_name['initial_interval']._options = None
  _QUICKEEPALIVESETTINGS.fields_by_name['initial_interval']._serialized_options = b'\372B\t\252\001\006\"\0002\002\010\001'
  _QUICPROTOCOLOPTIONS.fields_by_name['max_concurrent_streams']._options = None
  _QUICPROTOCOLOPTIONS.fields_by_name['max_concurrent_streams']._serialized_options = b'\372B\004*\002(\001'
  _QUICPROTOCOLOPTIONS.fields_by_name['initial_stream_window_size']._options = None
  _QUICPROTOCOLOPTIONS.fields_by_name['initial_stream_window_size']._serialized_options = b'\372B\t*\007\030\200\200\200\010(\001'
  _QUICPROTOCOLOPTIONS.fields_by_name['initial_connection_window_size']._options = None
  _QUICPROTOCOLOPTIONS.fields_by_name['initial_connection_window_size']._serialized_options = b'\372B\t*\007\030\200\200\200\014(\001'
  _QUICPROTOCOLOPTIONS.fields_by_name['num_timeouts_to_trigger_port_migration']._options = None
  _QUICPROTOCOLOPTIONS.fields_by_name['num_timeouts_to_trigger_port_migration']._serialized_options = b'\372B\006*\004\030\005(\000'
  _UPSTREAMHTTPPROTOCOLOPTIONS.fields_by_name['override_auto_sni_header']._options = None
  _UPSTREAMHTTPPROTOCOLOPTIONS.fields_by_name['override_auto_sni_header']._serialized_options = b'\372B\010r\006\300\001\001\320\001\001'
  _UPSTREAMHTTPPROTOCOLOPTIONS._options = None
  _UPSTREAMHTTPPROTOCOLOPTIONS._serialized_options = b'\232\305\210\036/\n-envoy.api.v2.core.UpstreamHttpProtocolOptions'
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY.fields_by_name['hostname']._options = None
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY.fields_by_name['hostname']._serialized_options = b'\372B\010r\006\300\001\001\320\001\001'
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY.fields_by_name['port']._options = None
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY.fields_by_name['port']._serialized_options = b'\372B\010*\006\020\377\377\003 \000'
  _ALTERNATEPROTOCOLSCACHEOPTIONS.fields_by_name['name']._options = None
  _ALTERNATEPROTOCOLSCACHEOPTIONS.fields_by_name['name']._serialized_options = b'\372B\004r\002\020\001'
  _ALTERNATEPROTOCOLSCACHEOPTIONS.fields_by_name['max_entries']._options = None
  _ALTERNATEPROTOCOLSCACHEOPTIONS.fields_by_name['max_entries']._serialized_options = b'\372B\004*\002 \000'
  _HTTPPROTOCOLOPTIONS.fields_by_name['max_headers_count']._options = None
  _HTTPPROTOCOLOPTIONS.fields_by_name['max_headers_count']._serialized_options = b'\372B\004*\002(\001'
  _HTTPPROTOCOLOPTIONS._options = None
  _HTTPPROTOCOLOPTIONS._serialized_options = b'\232\305\210\036\'\n%envoy.api.v2.core.HttpProtocolOptions'
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS._options = None
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS._serialized_options = b'\232\305\210\036H\nFenvoy.api.v2.core.Http1ProtocolOptions.HeaderKeyFormat.ProperCaseWords'
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT.oneofs_by_name['header_format']._options = None
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT.oneofs_by_name['header_format']._serialized_options = b'\370B\001'
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT._options = None
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT._serialized_options = b'\232\305\210\0368\n6envoy.api.v2.core.Http1ProtocolOptions.HeaderKeyFormat'
  _HTTP1PROTOCOLOPTIONS._options = None
  _HTTP1PROTOCOLOPTIONS._serialized_options = b'\232\305\210\036(\n&envoy.api.v2.core.Http1ProtocolOptions'
  _KEEPALIVESETTINGS.fields_by_name['interval']._options = None
  _KEEPALIVESETTINGS.fields_by_name['interval']._serialized_options = b'\372B\t\252\001\0062\004\020\300\204='
  _KEEPALIVESETTINGS.fields_by_name['timeout']._options = None
  _KEEPALIVESETTINGS.fields_by_name['timeout']._serialized_options = b'\372B\013\252\001\010\010\0012\004\020\300\204='
  _KEEPALIVESETTINGS.fields_by_name['connection_idle_interval']._options = None
  _KEEPALIVESETTINGS.fields_by_name['connection_idle_interval']._serialized_options = b'\372B\t\252\001\0062\004\020\300\204='
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER.fields_by_name['identifier']._options = None
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER.fields_by_name['identifier']._serialized_options = b'\372B\010*\006\030\377\377\003(\000\372B\005\212\001\002\020\001'
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER.fields_by_name['value']._options = None
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER.fields_by_name['value']._serialized_options = b'\372B\005\212\001\002\020\001'
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER._options = None
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER._serialized_options = b'\232\305\210\036:\n8envoy.api.v2.core.Http2ProtocolOptions.SettingsParameter'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_concurrent_streams']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_concurrent_streams']._serialized_options = b'\372B\n*\010\030\377\377\377\377\007(\001'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['initial_stream_window_size']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['initial_stream_window_size']._serialized_options = b'\372B\014*\n\030\377\377\377\377\007(\377\377\003'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['initial_connection_window_size']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['initial_connection_window_size']._serialized_options = b'\372B\014*\n\030\377\377\377\377\007(\377\377\003'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_outbound_frames']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_outbound_frames']._serialized_options = b'\372B\004*\002(\001'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_outbound_control_frames']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_outbound_control_frames']._serialized_options = b'\372B\004*\002(\001'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_inbound_window_update_frames_per_data_frame_sent']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['max_inbound_window_update_frames_per_data_frame_sent']._serialized_options = b'\372B\004*\002(\001'
  _HTTP2PROTOCOLOPTIONS.fields_by_name['stream_error_on_invalid_http_messaging']._options = None
  _HTTP2PROTOCOLOPTIONS.fields_by_name['stream_error_on_invalid_http_messaging']._serialized_options = b'\030\001\222\307\206\330\004\0033.0'
  _HTTP2PROTOCOLOPTIONS._options = None
  _HTTP2PROTOCOLOPTIONS._serialized_options = b'\232\305\210\036(\n&envoy.api.v2.core.Http2ProtocolOptions'
  _GRPCPROTOCOLOPTIONS._options = None
  _GRPCPROTOCOLOPTIONS._serialized_options = b'\232\305\210\036\'\n%envoy.api.v2.core.GrpcProtocolOptions'
  _HTTP3PROTOCOLOPTIONS.fields_by_name['allow_extended_connect']._options = None
  _HTTP3PROTOCOLOPTIONS.fields_by_name['allow_extended_connect']._serialized_options = b'\322\306\244\341\006\002\010\001'
  _SCHEMEHEADERTRANSFORMATION.fields_by_name['scheme_to_overwrite']._options = None
  _SCHEMEHEADERTRANSFORMATION.fields_by_name['scheme_to_overwrite']._serialized_options = b'\372B\017r\rR\004httpR\005https'
  _TCPPROTOCOLOPTIONS._serialized_start=353
  _TCPPROTOCOLOPTIONS._serialized_end=418
  _QUICKEEPALIVESETTINGS._serialized_start=421
  _QUICKEEPALIVESETTINGS._serialized_end=574
  _QUICPROTOCOLOPTIONS._serialized_start=577
  _QUICPROTOCOLOPTIONS._serialized_end=997
  _UPSTREAMHTTPPROTOCOLOPTIONS._serialized_start=1000
  _UPSTREAMHTTPPROTOCOLOPTIONS._serialized_end=1177
  _ALTERNATEPROTOCOLSCACHEOPTIONS._serialized_start=1180
  _ALTERNATEPROTOCOLSCACHEOPTIONS._serialized_end=1602
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY._serialized_start=1514
  _ALTERNATEPROTOCOLSCACHEOPTIONS_ALTERNATEPROTOCOLSCACHEENTRY._serialized_end=1602
  _HTTPPROTOCOLOPTIONS._serialized_start=1605
  _HTTPPROTOCOLOPTIONS._serialized_end=2163
  _HTTPPROTOCOLOPTIONS_HEADERSWITHUNDERSCORESACTION._serialized_start=2039
  _HTTPPROTOCOLOPTIONS_HEADERSWITHUNDERSCORESACTION._serialized_end=2117
  _HTTP1PROTOCOLOPTIONS._serialized_start=2166
  _HTTP1PROTOCOLOPTIONS._serialized_end=2990
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT._serialized_start=2564
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT._serialized_end=2943
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS._serialized_start=2762
  _HTTP1PROTOCOLOPTIONS_HEADERKEYFORMAT_PROPERCASEWORDS._serialized_end=2858
  _KEEPALIVESETTINGS._serialized_start=2993
  _KEEPALIVESETTINGS._serialized_end=3255
  _HTTP2PROTOCOLOPTIONS._serialized_start=3258
  _HTTP2PROTOCOLOPTIONS._serialized_end=4615
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER._serialized_start=4358
  _HTTP2PROTOCOLOPTIONS_SETTINGSPARAMETER._serialized_end=4568
  _GRPCPROTOCOLOPTIONS._serialized_start=4618
  _GRPCPROTOCOLOPTIONS._serialized_end=4761
  _HTTP3PROTOCOLOPTIONS._serialized_start=4764
  _HTTP3PROTOCOLOPTIONS._serialized_end=4985
  _SCHEMEHEADERTRANSFORMATION._serialized_start=4987
  _SCHEMEHEADERTRANSFORMATION._serialized_end=5084
# @@protoc_insertion_point(module_scope)
