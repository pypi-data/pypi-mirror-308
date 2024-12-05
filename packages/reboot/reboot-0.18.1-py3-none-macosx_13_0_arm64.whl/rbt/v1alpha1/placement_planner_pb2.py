# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: rbt/v1alpha1/placement_planner.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$rbt/v1alpha1/placement_planner.proto\x12\x0crbt.v1alpha1\"\x16\n\x14ListenForPlanRequest\"g\n\x15ListenForPlanResponse\x12 \n\x04plan\x18\x01 \x01(\x0b\x32\x12.rbt.v1alpha1.Plan\x12,\n\x0b\x63onsensuses\x18\x02 \x03(\x0b\x32\x17.rbt.v1alpha1.Consensus\"\x9e\x03\n\x04Plan\x12\x0f\n\x07version\x18\x01 \x01(\x03\x12\x34\n\x0c\x61pplications\x18\x02 \x03(\x0b\x32\x1e.rbt.v1alpha1.Plan.Application\x1a\xce\x02\n\x0b\x41pplication\x12\n\n\x02id\x18\x01 \x01(\t\x12\x38\n\x08services\x18\x02 \x03(\x0b\x32&.rbt.v1alpha1.Plan.Application.Service\x12\x34\n\x06shards\x18\x03 \x03(\x0b\x32$.rbt.v1alpha1.Plan.Application.Shard\x1a:\n\x07Service\x12\x11\n\tfull_name\x18\x01 \x01(\t\x12\x1c\n\x14state_type_full_name\x18\x02 \x01(\t\x1a\x86\x01\n\x05Shard\x12\n\n\x02id\x18\x01 \x01(\t\x12<\n\x05range\x18\x02 \x01(\x0b\x32-.rbt.v1alpha1.Plan.Application.Shard.KeyRange\x12\x14\n\x0c\x63onsensus_id\x18\x03 \x01(\t\x1a\x1d\n\x08KeyRange\x12\x11\n\tfirst_key\x18\x01 \x01(\x0c\"\x9b\x01\n\tConsensus\x12\n\n\x02id\x18\x01 \x01(\t\x12\x16\n\x0e\x61pplication_id\x18\x05 \x01(\t\x12\x30\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x1f.rbt.v1alpha1.Consensus.Address\x12\x11\n\tnamespace\x18\x04 \x01(\t\x1a%\n\x07\x41\x64\x64ress\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x0c\n\x04port\x18\x02 \x01(\x05\x32n\n\x10PlacementPlanner\x12Z\n\rListenForPlan\x12\".rbt.v1alpha1.ListenForPlanRequest\x1a#.rbt.v1alpha1.ListenForPlanResponse0\x01\x62\x06proto3')



_LISTENFORPLANREQUEST = DESCRIPTOR.message_types_by_name['ListenForPlanRequest']
_LISTENFORPLANRESPONSE = DESCRIPTOR.message_types_by_name['ListenForPlanResponse']
_PLAN = DESCRIPTOR.message_types_by_name['Plan']
_PLAN_APPLICATION = _PLAN.nested_types_by_name['Application']
_PLAN_APPLICATION_SERVICE = _PLAN_APPLICATION.nested_types_by_name['Service']
_PLAN_APPLICATION_SHARD = _PLAN_APPLICATION.nested_types_by_name['Shard']
_PLAN_APPLICATION_SHARD_KEYRANGE = _PLAN_APPLICATION_SHARD.nested_types_by_name['KeyRange']
_CONSENSUS = DESCRIPTOR.message_types_by_name['Consensus']
_CONSENSUS_ADDRESS = _CONSENSUS.nested_types_by_name['Address']
ListenForPlanRequest = _reflection.GeneratedProtocolMessageType('ListenForPlanRequest', (_message.Message,), {
  'DESCRIPTOR' : _LISTENFORPLANREQUEST,
  '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.ListenForPlanRequest)
  })
_sym_db.RegisterMessage(ListenForPlanRequest)

ListenForPlanResponse = _reflection.GeneratedProtocolMessageType('ListenForPlanResponse', (_message.Message,), {
  'DESCRIPTOR' : _LISTENFORPLANRESPONSE,
  '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.ListenForPlanResponse)
  })
_sym_db.RegisterMessage(ListenForPlanResponse)

Plan = _reflection.GeneratedProtocolMessageType('Plan', (_message.Message,), {

  'Application' : _reflection.GeneratedProtocolMessageType('Application', (_message.Message,), {

    'Service' : _reflection.GeneratedProtocolMessageType('Service', (_message.Message,), {
      'DESCRIPTOR' : _PLAN_APPLICATION_SERVICE,
      '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
      # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Plan.Application.Service)
      })
    ,

    'Shard' : _reflection.GeneratedProtocolMessageType('Shard', (_message.Message,), {

      'KeyRange' : _reflection.GeneratedProtocolMessageType('KeyRange', (_message.Message,), {
        'DESCRIPTOR' : _PLAN_APPLICATION_SHARD_KEYRANGE,
        '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
        # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Plan.Application.Shard.KeyRange)
        })
      ,
      'DESCRIPTOR' : _PLAN_APPLICATION_SHARD,
      '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
      # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Plan.Application.Shard)
      })
    ,
    'DESCRIPTOR' : _PLAN_APPLICATION,
    '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
    # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Plan.Application)
    })
  ,
  'DESCRIPTOR' : _PLAN,
  '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Plan)
  })
_sym_db.RegisterMessage(Plan)
_sym_db.RegisterMessage(Plan.Application)
_sym_db.RegisterMessage(Plan.Application.Service)
_sym_db.RegisterMessage(Plan.Application.Shard)
_sym_db.RegisterMessage(Plan.Application.Shard.KeyRange)

Consensus = _reflection.GeneratedProtocolMessageType('Consensus', (_message.Message,), {

  'Address' : _reflection.GeneratedProtocolMessageType('Address', (_message.Message,), {
    'DESCRIPTOR' : _CONSENSUS_ADDRESS,
    '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
    # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Consensus.Address)
    })
  ,
  'DESCRIPTOR' : _CONSENSUS,
  '__module__' : 'rbt.v1alpha1.placement_planner_pb2'
  # @@protoc_insertion_point(class_scope:rbt.v1alpha1.Consensus)
  })
_sym_db.RegisterMessage(Consensus)
_sym_db.RegisterMessage(Consensus.Address)

_PLACEMENTPLANNER = DESCRIPTOR.services_by_name['PlacementPlanner']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _LISTENFORPLANREQUEST._serialized_start=54
  _LISTENFORPLANREQUEST._serialized_end=76
  _LISTENFORPLANRESPONSE._serialized_start=78
  _LISTENFORPLANRESPONSE._serialized_end=181
  _PLAN._serialized_start=184
  _PLAN._serialized_end=598
  _PLAN_APPLICATION._serialized_start=264
  _PLAN_APPLICATION._serialized_end=598
  _PLAN_APPLICATION_SERVICE._serialized_start=403
  _PLAN_APPLICATION_SERVICE._serialized_end=461
  _PLAN_APPLICATION_SHARD._serialized_start=464
  _PLAN_APPLICATION_SHARD._serialized_end=598
  _PLAN_APPLICATION_SHARD_KEYRANGE._serialized_start=569
  _PLAN_APPLICATION_SHARD_KEYRANGE._serialized_end=598
  _CONSENSUS._serialized_start=601
  _CONSENSUS._serialized_end=756
  _CONSENSUS_ADDRESS._serialized_start=719
  _CONSENSUS_ADDRESS._serialized_end=756
  _PLACEMENTPLANNER._serialized_start=758
  _PLACEMENTPLANNER._serialized_end=868
# @@protoc_insertion_point(module_scope)
