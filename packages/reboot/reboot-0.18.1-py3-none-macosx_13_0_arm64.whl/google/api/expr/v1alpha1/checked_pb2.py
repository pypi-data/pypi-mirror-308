# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/api/expr/v1alpha1/checked.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api.expr.v1alpha1 import syntax_pb2 as google_dot_api_dot_expr_dot_v1alpha1_dot_syntax__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n&google/api/expr/v1alpha1/checked.proto\x12\x18google.api.expr.v1alpha1\x1a%google/api/expr/v1alpha1/syntax.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\"\xb6\x03\n\x0b\x43heckedExpr\x12N\n\rreference_map\x18\x02 \x03(\x0b\x32\x37.google.api.expr.v1alpha1.CheckedExpr.ReferenceMapEntry\x12\x44\n\x08type_map\x18\x03 \x03(\x0b\x32\x32.google.api.expr.v1alpha1.CheckedExpr.TypeMapEntry\x12\x39\n\x0bsource_info\x18\x05 \x01(\x0b\x32$.google.api.expr.v1alpha1.SourceInfo\x12,\n\x04\x65xpr\x18\x04 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Expr\x1aX\n\x11ReferenceMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\x32\n\x05value\x18\x02 \x01(\x0b\x32#.google.api.expr.v1alpha1.Reference:\x02\x38\x01\x1aN\n\x0cTypeMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12-\n\x05value\x18\x02 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type:\x02\x38\x01\"\x82\n\n\x04Type\x12%\n\x03\x64yn\x18\x01 \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12*\n\x04null\x18\x02 \x01(\x0e\x32\x1a.google.protobuf.NullValueH\x00\x12\x41\n\tprimitive\x18\x03 \x01(\x0e\x32,.google.api.expr.v1alpha1.Type.PrimitiveTypeH\x00\x12?\n\x07wrapper\x18\x04 \x01(\x0e\x32,.google.api.expr.v1alpha1.Type.PrimitiveTypeH\x00\x12\x42\n\nwell_known\x18\x05 \x01(\x0e\x32,.google.api.expr.v1alpha1.Type.WellKnownTypeH\x00\x12<\n\tlist_type\x18\x06 \x01(\x0b\x32\'.google.api.expr.v1alpha1.Type.ListTypeH\x00\x12:\n\x08map_type\x18\x07 \x01(\x0b\x32&.google.api.expr.v1alpha1.Type.MapTypeH\x00\x12?\n\x08\x66unction\x18\x08 \x01(\x0b\x32+.google.api.expr.v1alpha1.Type.FunctionTypeH\x00\x12\x16\n\x0cmessage_type\x18\t \x01(\tH\x00\x12\x14\n\ntype_param\x18\n \x01(\tH\x00\x12.\n\x04type\x18\x0b \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.TypeH\x00\x12\'\n\x05\x65rror\x18\x0c \x01(\x0b\x32\x16.google.protobuf.EmptyH\x00\x12\x44\n\rabstract_type\x18\x0e \x01(\x0b\x32+.google.api.expr.v1alpha1.Type.AbstractTypeH\x00\x1a=\n\x08ListType\x12\x31\n\telem_type\x18\x01 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x1ao\n\x07MapType\x12\x30\n\x08key_type\x18\x01 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x12\x32\n\nvalue_type\x18\x02 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x1av\n\x0c\x46unctionType\x12\x33\n\x0bresult_type\x18\x01 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x12\x31\n\targ_types\x18\x02 \x03(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x1aU\n\x0c\x41\x62stractType\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x37\n\x0fparameter_types\x18\x02 \x03(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\"s\n\rPrimitiveType\x12\x1e\n\x1aPRIMITIVE_TYPE_UNSPECIFIED\x10\x00\x12\x08\n\x04\x42OOL\x10\x01\x12\t\n\x05INT64\x10\x02\x12\n\n\x06UINT64\x10\x03\x12\n\n\x06\x44OUBLE\x10\x04\x12\n\n\x06STRING\x10\x05\x12\t\n\x05\x42YTES\x10\x06\"V\n\rWellKnownType\x12\x1f\n\x1bWELL_KNOWN_TYPE_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41NY\x10\x01\x12\r\n\tTIMESTAMP\x10\x02\x12\x0c\n\x08\x44URATION\x10\x03\x42\x0b\n\ttype_kind\"\xb9\x04\n\x04\x44\x65\x63l\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x39\n\x05ident\x18\x02 \x01(\x0b\x32(.google.api.expr.v1alpha1.Decl.IdentDeclH\x00\x12?\n\x08\x66unction\x18\x03 \x01(\x0b\x32+.google.api.expr.v1alpha1.Decl.FunctionDeclH\x00\x1ay\n\tIdentDecl\x12,\n\x04type\x18\x01 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".google.api.expr.v1alpha1.Constant\x12\x0b\n\x03\x64oc\x18\x03 \x01(\t\x1a\x9e\x02\n\x0c\x46unctionDecl\x12G\n\toverloads\x18\x01 \x03(\x0b\x32\x34.google.api.expr.v1alpha1.Decl.FunctionDecl.Overload\x1a\xc4\x01\n\x08Overload\x12\x13\n\x0boverload_id\x18\x01 \x01(\t\x12.\n\x06params\x18\x02 \x03(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x12\x13\n\x0btype_params\x18\x03 \x03(\t\x12\x33\n\x0bresult_type\x18\x04 \x01(\x0b\x32\x1e.google.api.expr.v1alpha1.Type\x12\x1c\n\x14is_instance_function\x18\x05 \x01(\x08\x12\x0b\n\x03\x64oc\x18\x06 \x01(\tB\x0b\n\tdecl_kind\"a\n\tReference\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x13\n\x0boverload_id\x18\x03 \x03(\t\x12\x31\n\x05value\x18\x04 \x01(\x0b\x32\".google.api.expr.v1alpha1.ConstantBl\n\x1c\x63om.google.api.expr.v1alpha1B\tDeclProtoP\x01Z<google.golang.org/genproto/googleapis/api/expr/v1alpha1;expr\xf8\x01\x01\x62\x06proto3')



_CHECKEDEXPR = DESCRIPTOR.message_types_by_name['CheckedExpr']
_CHECKEDEXPR_REFERENCEMAPENTRY = _CHECKEDEXPR.nested_types_by_name['ReferenceMapEntry']
_CHECKEDEXPR_TYPEMAPENTRY = _CHECKEDEXPR.nested_types_by_name['TypeMapEntry']
_TYPE = DESCRIPTOR.message_types_by_name['Type']
_TYPE_LISTTYPE = _TYPE.nested_types_by_name['ListType']
_TYPE_MAPTYPE = _TYPE.nested_types_by_name['MapType']
_TYPE_FUNCTIONTYPE = _TYPE.nested_types_by_name['FunctionType']
_TYPE_ABSTRACTTYPE = _TYPE.nested_types_by_name['AbstractType']
_DECL = DESCRIPTOR.message_types_by_name['Decl']
_DECL_IDENTDECL = _DECL.nested_types_by_name['IdentDecl']
_DECL_FUNCTIONDECL = _DECL.nested_types_by_name['FunctionDecl']
_DECL_FUNCTIONDECL_OVERLOAD = _DECL_FUNCTIONDECL.nested_types_by_name['Overload']
_REFERENCE = DESCRIPTOR.message_types_by_name['Reference']
_TYPE_PRIMITIVETYPE = _TYPE.enum_types_by_name['PrimitiveType']
_TYPE_WELLKNOWNTYPE = _TYPE.enum_types_by_name['WellKnownType']
CheckedExpr = _reflection.GeneratedProtocolMessageType('CheckedExpr', (_message.Message,), {

  'ReferenceMapEntry' : _reflection.GeneratedProtocolMessageType('ReferenceMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _CHECKEDEXPR_REFERENCEMAPENTRY,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.CheckedExpr.ReferenceMapEntry)
    })
  ,

  'TypeMapEntry' : _reflection.GeneratedProtocolMessageType('TypeMapEntry', (_message.Message,), {
    'DESCRIPTOR' : _CHECKEDEXPR_TYPEMAPENTRY,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.CheckedExpr.TypeMapEntry)
    })
  ,
  'DESCRIPTOR' : _CHECKEDEXPR,
  '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
  # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.CheckedExpr)
  })
_sym_db.RegisterMessage(CheckedExpr)
_sym_db.RegisterMessage(CheckedExpr.ReferenceMapEntry)
_sym_db.RegisterMessage(CheckedExpr.TypeMapEntry)

Type = _reflection.GeneratedProtocolMessageType('Type', (_message.Message,), {

  'ListType' : _reflection.GeneratedProtocolMessageType('ListType', (_message.Message,), {
    'DESCRIPTOR' : _TYPE_LISTTYPE,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Type.ListType)
    })
  ,

  'MapType' : _reflection.GeneratedProtocolMessageType('MapType', (_message.Message,), {
    'DESCRIPTOR' : _TYPE_MAPTYPE,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Type.MapType)
    })
  ,

  'FunctionType' : _reflection.GeneratedProtocolMessageType('FunctionType', (_message.Message,), {
    'DESCRIPTOR' : _TYPE_FUNCTIONTYPE,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Type.FunctionType)
    })
  ,

  'AbstractType' : _reflection.GeneratedProtocolMessageType('AbstractType', (_message.Message,), {
    'DESCRIPTOR' : _TYPE_ABSTRACTTYPE,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Type.AbstractType)
    })
  ,
  'DESCRIPTOR' : _TYPE,
  '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
  # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Type)
  })
_sym_db.RegisterMessage(Type)
_sym_db.RegisterMessage(Type.ListType)
_sym_db.RegisterMessage(Type.MapType)
_sym_db.RegisterMessage(Type.FunctionType)
_sym_db.RegisterMessage(Type.AbstractType)

Decl = _reflection.GeneratedProtocolMessageType('Decl', (_message.Message,), {

  'IdentDecl' : _reflection.GeneratedProtocolMessageType('IdentDecl', (_message.Message,), {
    'DESCRIPTOR' : _DECL_IDENTDECL,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Decl.IdentDecl)
    })
  ,

  'FunctionDecl' : _reflection.GeneratedProtocolMessageType('FunctionDecl', (_message.Message,), {

    'Overload' : _reflection.GeneratedProtocolMessageType('Overload', (_message.Message,), {
      'DESCRIPTOR' : _DECL_FUNCTIONDECL_OVERLOAD,
      '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
      # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Decl.FunctionDecl.Overload)
      })
    ,
    'DESCRIPTOR' : _DECL_FUNCTIONDECL,
    '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
    # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Decl.FunctionDecl)
    })
  ,
  'DESCRIPTOR' : _DECL,
  '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
  # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Decl)
  })
_sym_db.RegisterMessage(Decl)
_sym_db.RegisterMessage(Decl.IdentDecl)
_sym_db.RegisterMessage(Decl.FunctionDecl)
_sym_db.RegisterMessage(Decl.FunctionDecl.Overload)

Reference = _reflection.GeneratedProtocolMessageType('Reference', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCE,
  '__module__' : 'google.api.expr.v1alpha1.checked_pb2'
  # @@protoc_insertion_point(class_scope:google.api.expr.v1alpha1.Reference)
  })
_sym_db.RegisterMessage(Reference)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034com.google.api.expr.v1alpha1B\tDeclProtoP\001Z<google.golang.org/genproto/googleapis/api/expr/v1alpha1;expr\370\001\001'
  _CHECKEDEXPR_REFERENCEMAPENTRY._options = None
  _CHECKEDEXPR_REFERENCEMAPENTRY._serialized_options = b'8\001'
  _CHECKEDEXPR_TYPEMAPENTRY._options = None
  _CHECKEDEXPR_TYPEMAPENTRY._serialized_options = b'8\001'
  _CHECKEDEXPR._serialized_start=167
  _CHECKEDEXPR._serialized_end=605
  _CHECKEDEXPR_REFERENCEMAPENTRY._serialized_start=437
  _CHECKEDEXPR_REFERENCEMAPENTRY._serialized_end=525
  _CHECKEDEXPR_TYPEMAPENTRY._serialized_start=527
  _CHECKEDEXPR_TYPEMAPENTRY._serialized_end=605
  _TYPE._serialized_start=608
  _TYPE._serialized_end=1890
  _TYPE_LISTTYPE._serialized_start=1291
  _TYPE_LISTTYPE._serialized_end=1352
  _TYPE_MAPTYPE._serialized_start=1354
  _TYPE_MAPTYPE._serialized_end=1465
  _TYPE_FUNCTIONTYPE._serialized_start=1467
  _TYPE_FUNCTIONTYPE._serialized_end=1585
  _TYPE_ABSTRACTTYPE._serialized_start=1587
  _TYPE_ABSTRACTTYPE._serialized_end=1672
  _TYPE_PRIMITIVETYPE._serialized_start=1674
  _TYPE_PRIMITIVETYPE._serialized_end=1789
  _TYPE_WELLKNOWNTYPE._serialized_start=1791
  _TYPE_WELLKNOWNTYPE._serialized_end=1877
  _DECL._serialized_start=1893
  _DECL._serialized_end=2462
  _DECL_IDENTDECL._serialized_start=2039
  _DECL_IDENTDECL._serialized_end=2160
  _DECL_FUNCTIONDECL._serialized_start=2163
  _DECL_FUNCTIONDECL._serialized_end=2449
  _DECL_FUNCTIONDECL_OVERLOAD._serialized_start=2253
  _DECL_FUNCTIONDECL_OVERLOAD._serialized_end=2449
  _REFERENCE._serialized_start=2464
  _REFERENCE._serialized_end=2561
# @@protoc_insertion_point(module_scope)
