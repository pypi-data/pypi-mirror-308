# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: xds/type/matcher/v3/regex.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from validate import validate_pb2 as validate_dot_validate__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fxds/type/matcher/v3/regex.proto\x12\x13xds.type.matcher.v3\x1a\x17validate/validate.proto\"\x94\x01\n\x0cRegexMatcher\x12K\n\ngoogle_re2\x18\x01 \x01(\x0b\x32+.xds.type.matcher.v3.RegexMatcher.GoogleRE2B\x08\xfa\x42\x05\x8a\x01\x02\x10\x01H\x00\x12\x16\n\x05regex\x18\x02 \x01(\tB\x07\xfa\x42\x04r\x02\x10\x01\x1a\x0b\n\tGoogleRE2B\x12\n\x0b\x65ngine_type\x12\x03\xf8\x42\x01\x42Z\n\x1e\x63om.github.xds.type.matcher.v3B\nRegexProtoP\x01Z*github.com/cncf/xds/go/xds/type/matcher/v3b\x06proto3')



_REGEXMATCHER = DESCRIPTOR.message_types_by_name['RegexMatcher']
_REGEXMATCHER_GOOGLERE2 = _REGEXMATCHER.nested_types_by_name['GoogleRE2']
RegexMatcher = _reflection.GeneratedProtocolMessageType('RegexMatcher', (_message.Message,), {

  'GoogleRE2' : _reflection.GeneratedProtocolMessageType('GoogleRE2', (_message.Message,), {
    'DESCRIPTOR' : _REGEXMATCHER_GOOGLERE2,
    '__module__' : 'xds.type.matcher.v3.regex_pb2'
    # @@protoc_insertion_point(class_scope:xds.type.matcher.v3.RegexMatcher.GoogleRE2)
    })
  ,
  'DESCRIPTOR' : _REGEXMATCHER,
  '__module__' : 'xds.type.matcher.v3.regex_pb2'
  # @@protoc_insertion_point(class_scope:xds.type.matcher.v3.RegexMatcher)
  })
_sym_db.RegisterMessage(RegexMatcher)
_sym_db.RegisterMessage(RegexMatcher.GoogleRE2)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\036com.github.xds.type.matcher.v3B\nRegexProtoP\001Z*github.com/cncf/xds/go/xds/type/matcher/v3'
  _REGEXMATCHER.oneofs_by_name['engine_type']._options = None
  _REGEXMATCHER.oneofs_by_name['engine_type']._serialized_options = b'\370B\001'
  _REGEXMATCHER.fields_by_name['google_re2']._options = None
  _REGEXMATCHER.fields_by_name['google_re2']._serialized_options = b'\372B\005\212\001\002\020\001'
  _REGEXMATCHER.fields_by_name['regex']._options = None
  _REGEXMATCHER.fields_by_name['regex']._serialized_options = b'\372B\004r\002\020\001'
  _REGEXMATCHER._serialized_start=82
  _REGEXMATCHER._serialized_end=230
  _REGEXMATCHER_GOOGLERE2._serialized_start=199
  _REGEXMATCHER_GOOGLERE2._serialized_end=210
# @@protoc_insertion_point(module_scope)
