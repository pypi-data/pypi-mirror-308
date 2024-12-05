# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: envoy/type/matcher/v3/value.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from envoy.type.matcher.v3 import number_pb2 as envoy_dot_type_dot_matcher_dot_v3_dot_number__pb2
from envoy.type.matcher.v3 import string_pb2 as envoy_dot_type_dot_matcher_dot_v3_dot_string__pb2
from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from udpa.annotations import versioning_pb2 as udpa_dot_annotations_dot_versioning__pb2
from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n!envoy/type/matcher/v3/value.proto\x12\x15\x65nvoy.type.matcher.v3\x1a\"envoy/type/matcher/v3/number.proto\x1a\"envoy/type/matcher/v3/string.proto\x1a\x1dudpa/annotations/status.proto\x1a!udpa/annotations/versioning.proto\x1a\x17validate/validate.proto\"\xb5\x03\n\x0cValueMatcher\x12\x43\n\nnull_match\x18\x01 \x01(\x0b\x32-.envoy.type.matcher.v3.ValueMatcher.NullMatchH\x00\x12<\n\x0c\x64ouble_match\x18\x02 \x01(\x0b\x32$.envoy.type.matcher.v3.DoubleMatcherH\x00\x12<\n\x0cstring_match\x18\x03 \x01(\x0b\x32$.envoy.type.matcher.v3.StringMatcherH\x00\x12\x14\n\nbool_match\x18\x04 \x01(\x08H\x00\x12\x17\n\rpresent_match\x18\x05 \x01(\x08H\x00\x12\x38\n\nlist_match\x18\x06 \x01(\x0b\x32\".envoy.type.matcher.v3.ListMatcherH\x00\x1a=\n\tNullMatch:0\x9a\xc5\x88\x1e+\n)envoy.type.matcher.ValueMatcher.NullMatch:&\x9a\xc5\x88\x1e!\n\x1f\x65nvoy.type.matcher.ValueMatcherB\x14\n\rmatch_pattern\x12\x03\xf8\x42\x01\"\x81\x01\n\x0bListMatcher\x12\x35\n\x06one_of\x18\x01 \x01(\x0b\x32#.envoy.type.matcher.v3.ValueMatcherH\x00:%\x9a\xc5\x88\x1e \n\x1e\x65nvoy.type.matcher.ListMatcherB\x14\n\rmatch_pattern\x12\x03\xf8\x42\x01\x42\x83\x01\n#io.envoyproxy.envoy.type.matcher.v3B\nValueProtoP\x01ZFgithub.com/envoyproxy/go-control-plane/envoy/type/matcher/v3;matcherv3\xba\x80\xc8\xd1\x06\x02\x10\x02\x62\x06proto3')



_VALUEMATCHER = DESCRIPTOR.message_types_by_name['ValueMatcher']
_VALUEMATCHER_NULLMATCH = _VALUEMATCHER.nested_types_by_name['NullMatch']
_LISTMATCHER = DESCRIPTOR.message_types_by_name['ListMatcher']
ValueMatcher = _reflection.GeneratedProtocolMessageType('ValueMatcher', (_message.Message,), {

  'NullMatch' : _reflection.GeneratedProtocolMessageType('NullMatch', (_message.Message,), {
    'DESCRIPTOR' : _VALUEMATCHER_NULLMATCH,
    '__module__' : 'envoy.type.matcher.v3.value_pb2'
    # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.ValueMatcher.NullMatch)
    })
  ,
  'DESCRIPTOR' : _VALUEMATCHER,
  '__module__' : 'envoy.type.matcher.v3.value_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.ValueMatcher)
  })
_sym_db.RegisterMessage(ValueMatcher)
_sym_db.RegisterMessage(ValueMatcher.NullMatch)

ListMatcher = _reflection.GeneratedProtocolMessageType('ListMatcher', (_message.Message,), {
  'DESCRIPTOR' : _LISTMATCHER,
  '__module__' : 'envoy.type.matcher.v3.value_pb2'
  # @@protoc_insertion_point(class_scope:envoy.type.matcher.v3.ListMatcher)
  })
_sym_db.RegisterMessage(ListMatcher)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n#io.envoyproxy.envoy.type.matcher.v3B\nValueProtoP\001ZFgithub.com/envoyproxy/go-control-plane/envoy/type/matcher/v3;matcherv3\272\200\310\321\006\002\020\002'
  _VALUEMATCHER_NULLMATCH._options = None
  _VALUEMATCHER_NULLMATCH._serialized_options = b'\232\305\210\036+\n)envoy.type.matcher.ValueMatcher.NullMatch'
  _VALUEMATCHER.oneofs_by_name['match_pattern']._options = None
  _VALUEMATCHER.oneofs_by_name['match_pattern']._serialized_options = b'\370B\001'
  _VALUEMATCHER._options = None
  _VALUEMATCHER._serialized_options = b'\232\305\210\036!\n\037envoy.type.matcher.ValueMatcher'
  _LISTMATCHER.oneofs_by_name['match_pattern']._options = None
  _LISTMATCHER.oneofs_by_name['match_pattern']._serialized_options = b'\370B\001'
  _LISTMATCHER._options = None
  _LISTMATCHER._serialized_options = b'\232\305\210\036 \n\036envoy.type.matcher.ListMatcher'
  _VALUEMATCHER._serialized_start=224
  _VALUEMATCHER._serialized_end=661
  _VALUEMATCHER_NULLMATCH._serialized_start=538
  _VALUEMATCHER_NULLMATCH._serialized_end=599
  _LISTMATCHER._serialized_start=664
  _LISTMATCHER._serialized_end=793
# @@protoc_insertion_point(module_scope)
