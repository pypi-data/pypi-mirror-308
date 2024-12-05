# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/type/matcher/v3/http_inputs.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'envoy/type/matcher/v3/http_inputs.proto\x12\x15\x65nvoy.type.matcher.v3\x1a\x1dudpa/annotations/status.proto\x1a\x17validate/validate.proto\"?\n\x1bHttpRequestHeaderMatchInput\x12 \n\x0bheader_name\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xc8\x01\x00\"@\n\x1cHttpRequestTrailerMatchInput\x12 \n\x0bheader_name\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xc8\x01\x00\"@\n\x1cHttpResponseHeaderMatchInput\x12 \n\x0bheader_name\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xc8\x01\x00\"A\n\x1dHttpResponseTrailerMatchInput\x12 \n\x0bheader_name\x18\x01 \x01(\tB\x0b\xfa\x42\x08r\x06\xc0\x01\x01\xc8\x01\x00\"?\n\x1fHttpRequestQueryParamMatchInput\x12\x1c\n\x0bquery_param\x18\x01 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x42\x88\x01\n#io.envoyproxy.envoy.type.matcher.v3B\x0fHttpInputsProtoP\x01ZFgithub.com/envoyproxy/go-control-plane/envoy/type/matcher/v3;matcherv3\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_HTTPREQUESTHEADERMATCHINPUT = DESCRIPTOR.message_types_by_name['HttpRequestHeaderMatchInput']
_HTTPREQUESTTRAILERMATCHINPUT = DESCRIPTOR.message_types_by_name['HttpRequestTrailerMatchInput']
_HTTPRESPONSEHEADERMATCHINPUT = DESCRIPTOR.message_types_by_name['HttpResponseHeaderMatchInput']
_HTTPRESPONSETRAILERMATCHINPUT = DESCRIPTOR.message_types_by_name['HttpResponseTrailerMatchInput']
_HTTPREQUESTQUERYPARAMMATCHINPUT = DESCRIPTOR.message_types_by_name['HttpRequestQueryParamMatchInput']
HttpRequestHeaderMatchInput = _reflection.GeneratedProtocolMessageType('HttpRequestHeaderMatchInput', (_message.Message,), {
  'DESCRIPTOR' : _HTTPREQUESTHEADERMATCHINPUT,
  '__module__' : 'envoy.type.matcher.v3.http_inputs_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.HttpRequestHeaderMatchInput)
  })
_sym_db.RegisterMessage(HttpRequestHeaderMatchInput)

HttpRequestTrailerMatchInput = _reflection.GeneratedProtocolMessageType('HttpRequestTrailerMatchInput', (_message.Message,), {
  'DESCRIPTOR' : _HTTPREQUESTTRAILERMATCHINPUT,
  '__module__' : 'envoy.type.matcher.v3.http_inputs_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.HttpRequestTrailerMatchInput)
  })
_sym_db.RegisterMessage(HttpRequestTrailerMatchInput)

HttpResponseHeaderMatchInput = _reflection.GeneratedProtocolMessageType('HttpResponseHeaderMatchInput', (_message.Message,), {
  'DESCRIPTOR' : _HTTPRESPONSEHEADERMATCHINPUT,
  '__module__' : 'envoy.type.matcher.v3.http_inputs_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.HttpResponseHeaderMatchInput)
  })
_sym_db.RegisterMessage(HttpResponseHeaderMatchInput)

HttpResponseTrailerMatchInput = _reflection.GeneratedProtocolMessageType('HttpResponseTrailerMatchInput', (_message.Message,), {
  'DESCRIPTOR' : _HTTPRESPONSETRAILERMATCHINPUT,
  '__module__' : 'envoy.type.matcher.v3.http_inputs_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.HttpResponseTrailerMatchInput)
  })
_sym_db.RegisterMessage(HttpResponseTrailerMatchInput)

HttpRequestQueryParamMatchInput = _reflection.GeneratedProtocolMessageType('HttpRequestQueryParamMatchInput', (_message.Message,), {
  'DESCRIPTOR' : _HTTPREQUESTQUERYPARAMMATCHINPUT,
  '__module__' : 'envoy.type.matcher.v3.http_inputs_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.HttpRequestQueryParamMatchInput)
  })
_sym_db.RegisterMessage(HttpRequestQueryParamMatchInput)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#io.envoyproxy.envoy.type.matcher.v3B\017HttpInputsProtoP\001ZFgithub.com/envoyproxy/go-control-plane/envoy/type/matcher/v3;matcherv3\272\200\310\321\006\002\020\002'
  _HTTPREQUESTHEADERMATCHINPUT.fields_by_name['header_name']._options = None
  _HTTPREQUESTHEADERMATCHINPUT.fields_by_name['header_name']._serialized_options = b'\372B\010r\006\300\001\001\310\001\000'
  _HTTPREQUESTTRAILERMATCHINPUT.fields_by_name['header_name']._options = None
  _HTTPREQUESTTRAILERMATCHINPUT.fields_by_name['header_name']._serialized_options = b'\372B\010r\006\300\001\001\310\001\000'
  _HTTPRESPONSEHEADERMATCHINPUT.fields_by_name['header_name']._options = None
  _HTTPRESPONSEHEADERMATCHINPUT.fields_by_name['header_name']._serialized_options = b'\372B\010r\006\300\001\001\310\001\000'
  _HTTPRESPONSETRAILERMATCHINPUT.fields_by_name['header_name']._options = None
  _HTTPRESPONSETRAILERMATCHINPUT.fields_by_name['header_name']._serialized_options = b'\372B\010r\006\300\001\001\310\001\000'
  _HTTPREQUESTQUERYPARAMMATCHINPUT.fields_by_name['query_param']._options = None
  _HTTPREQUESTQUERYPARAMMATCHINPUT.fields_by_name['query_param']._serialized_options = b'\372B\004r\002\020\001'
  _HTTPREQUESTHEADERMATCHINPUT._serialized_start=122
  _HTTPREQUESTHEADERMATCHINPUT._serialized_end=185
  _HTTPREQUESTTRAILERMATCHINPUT._serialized_start=187
  _HTTPREQUESTTRAILERMATCHINPUT._serialized_end=251
  _HTTPRESPONSEHEADERMATCHINPUT._serialized_start=253
  _HTTPRESPONSEHEADERMATCHINPUT._serialized_end=317
  _HTTPRESPONSETRAILERMATCHINPUT._serialized_start=319
  _HTTPRESPONSETRAILERMATCHINPUT._serialized_end=384
  _HTTPREQUESTQUERYPARAMMATCHINPUT._serialized_start=386
  _HTTPREQUESTQUERYPARAMMATCHINPUT._serialized_end=449
# @@protoc_insertion_point(module_scope)
