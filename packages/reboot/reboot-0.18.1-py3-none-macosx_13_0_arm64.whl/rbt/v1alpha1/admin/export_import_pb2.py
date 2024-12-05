# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rbt/v1alpha1/admin/export_import.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&rbt/v1alpha1/admin/export_import.proto\x12\x12rbt.v1alpha1.admin\x1a\x1cgoogle/protobuf/struct.proto\"\x18\n\x16ListConsensusesRequest\"0\n\x17ListConsensusesResponse\x12\x15\n\rconsensus_ids\x18\x01 \x03(\t\"%\n\rExportRequest\x12\x14\n\x0c\x63onsensus_id\x18\x01 \x01(\t\"\xe8\x01\n\x10\x45xportImportItem\x12\x12\n\nstate_type\x18\x01 \x01(\t\x12\x11\n\tstate_ref\x18\x02 \x01(\t\x12(\n\x05state\x18\x03 \x01(\x0b\x32\x17.google.protobuf.StructH\x00\x12\x1a\n\x10sorted_map_entry\x18\x04 \x01(\x0cH\x00\x12\'\n\x04task\x18\x05 \x01(\x0b\x32\x17.google.protobuf.StructH\x00\x12\x36\n\x13idempotent_mutation\x18\x06 \x01(\x0b\x32\x17.google.protobuf.StructH\x00\x42\x06\n\x04item\"\x10\n\x0eImportResponse2\xa5\x02\n\x0c\x45xportImport\x12j\n\x0fListConsensuses\x12*.rbt.v1alpha1.admin.ListConsensusesRequest\x1a+.rbt.v1alpha1.admin.ListConsensusesResponse\x12S\n\x06\x45xport\x12!.rbt.v1alpha1.admin.ExportRequest\x1a$.rbt.v1alpha1.admin.ExportImportItem0\x01\x12T\n\x06Import\x12$.rbt.v1alpha1.admin.ExportImportItem\x1a\".rbt.v1alpha1.admin.ImportResponse(\x01\x62\x06proto3')



_LISTCONSENSUSESREQUEST = DESCRIPTOR.message_types_by_name['ListConsensusesRequest']
_LISTCONSENSUSESRESPONSE = DESCRIPTOR.message_types_by_name['ListConsensusesResponse']
_EXPORTREQUEST = DESCRIPTOR.message_types_by_name['ExportRequest']
_EXPORTIMPORTITEM = DESCRIPTOR.message_types_by_name['ExportImportItem']
_IMPORTRESPONSE = DESCRIPTOR.message_types_by_name['ImportResponse']
ListConsensusesRequest = _reflection.GeneratedProtocolMessageType('ListConsensusesRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONSENSUSESREQUEST,
  '__module__' : 'rbt.v1alpha1.admin.export_import_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.admin.ListConsensusesRequest)
  })
_sym_db.RegisterMessage(ListConsensusesRequest)

ListConsensusesResponse = _reflection.GeneratedProtocolMessageType('ListConsensusesResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTCONSENSUSESRESPONSE,
  '__module__' : 'rbt.v1alpha1.admin.export_import_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.admin.ListConsensusesResponse)
  })
_sym_db.RegisterMessage(ListConsensusesResponse)

ExportRequest = _reflection.GeneratedProtocolMessageType('ExportRequest', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTREQUEST,
  '__module__' : 'rbt.v1alpha1.admin.export_import_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.admin.ExportRequest)
  })
_sym_db.RegisterMessage(ExportRequest)

ExportImportItem = _reflection.GeneratedProtocolMessageType('ExportImportItem', (_message.Message,), {
  'DESCRIPTOR' : _EXPORTIMPORTITEM,
  '__module__' : 'rbt.v1alpha1.admin.export_import_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.admin.ExportImportItem)
  })
_sym_db.RegisterMessage(ExportImportItem)

ImportResponse = _reflection.GeneratedProtocolMessageType('ImportResponse', (_message.Message,), {
  'DESCRIPTOR' : _IMPORTRESPONSE,
  '__module__' : 'rbt.v1alpha1.admin.export_import_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.admin.ImportResponse)
  })
_sym_db.RegisterMessage(ImportResponse)

_EXPORTIMPORT = DESCRIPTOR.services_by_name['ExportImport']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LISTCONSENSUSESREQUEST._serialized_start=92
  _LISTCONSENSUSESREQUEST._serialized_end=116
  _LISTCONSENSUSESRESPONSE._serialized_start=118
  _LISTCONSENSUSESRESPONSE._serialized_end=166
  _EXPORTREQUEST._serialized_start=168
  _EXPORTREQUEST._serialized_end=205
  _EXPORTIMPORTITEM._serialized_start=208
  _EXPORTIMPORTITEM._serialized_end=440
  _IMPORTRESPONSE._serialized_start=442
  _IMPORTRESPONSE._serialized_end=458
  _EXPORTIMPORT._serialized_start=461
  _EXPORTIMPORT._serialized_end=754
# @@protoc_insertion_point(module_scope)
