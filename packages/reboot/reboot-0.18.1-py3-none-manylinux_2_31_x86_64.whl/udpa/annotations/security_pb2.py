# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: udpa/annotations/security.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from udpa.annotations import status_pb2 as udpa_dot_annotations_dot_status__pb2
from google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1fudpa/annotations/security.proto\x12\x10udpa.annotations\x1a\x1dudpa/annotations/status.proto\x1a google/protobuf/descriptor.proto\"o\n\x17\x46ieldSecurityAnnotation\x12*\n\"configure_for_untrusted_downstream\x18\x01 \x01(\x08\x12(\n configure_for_untrusted_upstream\x18\x02 \x01(\x08:]\n\x08security\x12\x1d.google.protobuf.FieldOptions\x18\xb1\xf2\xa6\x05 \x01(\x0b\x32).udpa.annotations.FieldSecurityAnnotationB,Z\"github.com/cncf/xds/go/annotations\xba\x80\xc8\xd1\x06\x02\x08\x01\x62\x06proto3')


SECURITY_FIELD_NUMBER = 11122993
security = DESCRIPTOR.extensions_by_name['security']

_FIELDSECURITYANNOTATION = DESCRIPTOR.message_types_by_name['FieldSecurityAnnotation']
FieldSecurityAnnotation = _reflection.GeneratedProtocolMessageType('FieldSecurityAnnotation', (_message.Message,), {
  'DESCRIPTOR' : _FIELDSECURITYANNOTATION,
  '__module__' : 'udpa.annotations.security_pb2'
  # @@protoc_insertion_point(class_scope:udpa.annotations.FieldSecurityAnnotation)
  })
_sym_db.RegisterMessage(FieldSecurityAnnotation)

if _descriptor._USE_C_DESCRIPTORS == False:
  google_dot_protobuf_dot_descriptor__pb2.FieldOptions.RegisterExtension(security)

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\"github.com/cncf/xds/go/annotations\272\200\310\321\006\002\010\001'
  _FIELDSECURITYANNOTATION._serialized_start=118
  _FIELDSECURITYANNOTATION._serialized_end=229
# @@protoc_insertion_point(module_scope)
