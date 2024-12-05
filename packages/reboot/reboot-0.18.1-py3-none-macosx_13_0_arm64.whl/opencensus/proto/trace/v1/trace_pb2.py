# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: opencensus/proto/trace/v1/trace.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from opencensus.proto.resource.v1 import resource_pb2 as opencensus_dot_proto_dot_resource_dot_v1_dot_resource__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%opencensus/proto/trace/v1/trace.proto\x12\x19opencensus.proto.trace.v1\x1a+opencensus/proto/resource/v1/resource.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\x1egoogle/protobuf/wrappers.proto\"\xac\x12\n\x04Span\x12\x10\n\x08trace_id\x18\x01 \x01(\x0c\x12\x0f\n\x07span_id\x18\x02 \x01(\x0c\x12>\n\ntracestate\x18\x0f \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.Tracestate\x12\x16\n\x0eparent_span_id\x18\x03 \x01(\x0c\x12:\n\x04name\x18\x04 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12\x36\n\x04kind\x18\x0e \x01(\x0e\x32(.opencensus.proto.trace.v1.Span.SpanKind\x12.\n\nstart_time\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12,\n\x08\x65nd_time\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12>\n\nattributes\x18\x07 \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.Attributes\x12:\n\x0bstack_trace\x18\x08 \x01(\x0b\x32%.opencensus.proto.trace.v1.StackTrace\x12?\n\x0btime_events\x18\t \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.TimeEvents\x12\x34\n\x05links\x18\n \x01(\x0b\x32%.opencensus.proto.trace.v1.Span.Links\x12\x31\n\x06status\x18\x0b \x01(\x0b\x32!.opencensus.proto.trace.v1.Status\x12\x38\n\x08resource\x18\x10 \x01(\x0b\x32&.opencensus.proto.resource.v1.Resource\x12?\n\x1bsame_process_as_parent_span\x18\x0c \x01(\x0b\x32\x1a.google.protobuf.BoolValue\x12\x36\n\x10\x63hild_span_count\x18\r \x01(\x0b\x32\x1c.google.protobuf.UInt32Value\x1at\n\nTracestate\x12\x41\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x30.opencensus.proto.trace.v1.Span.Tracestate.Entry\x1a#\n\x05\x45ntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\x1a\xe3\x01\n\nAttributes\x12S\n\rattribute_map\x18\x01 \x03(\x0b\x32<.opencensus.proto.trace.v1.Span.Attributes.AttributeMapEntry\x12 \n\x18\x64ropped_attributes_count\x18\x02 \x01(\x05\x1a^\n\x11\x41ttributeMapEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x38\n\x05value\x18\x02 \x01(\x0b\x32).opencensus.proto.trace.v1.AttributeValue:\x02\x38\x01\x1a\xbf\x04\n\tTimeEvent\x12(\n\x04time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12J\n\nannotation\x18\x02 \x01(\x0b\x32\x34.opencensus.proto.trace.v1.Span.TimeEvent.AnnotationH\x00\x12O\n\rmessage_event\x18\x03 \x01(\x0b\x32\x36.opencensus.proto.trace.v1.Span.TimeEvent.MessageEventH\x00\x1a\x8f\x01\n\nAnnotation\x12\x41\n\x0b\x64\x65scription\x18\x01 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12>\n\nattributes\x18\x02 \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.Attributes\x1a\xcf\x01\n\x0cMessageEvent\x12I\n\x04type\x18\x01 \x01(\x0e\x32;.opencensus.proto.trace.v1.Span.TimeEvent.MessageEvent.Type\x12\n\n\x02id\x18\x02 \x01(\x04\x12\x19\n\x11uncompressed_size\x18\x03 \x01(\x04\x12\x17\n\x0f\x63ompressed_size\x18\x04 \x01(\x04\"4\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x08\n\x04SENT\x10\x01\x12\x0c\n\x08RECEIVED\x10\x02\x42\x07\n\x05value\x1a\x94\x01\n\nTimeEvents\x12=\n\ntime_event\x18\x01 \x03(\x0b\x32).opencensus.proto.trace.v1.Span.TimeEvent\x12!\n\x19\x64ropped_annotations_count\x18\x02 \x01(\x05\x12$\n\x1c\x64ropped_message_events_count\x18\x03 \x01(\x05\x1a\xaf\x02\n\x04Link\x12\x10\n\x08trace_id\x18\x01 \x01(\x0c\x12\x0f\n\x07span_id\x18\x02 \x01(\x0c\x12\x37\n\x04type\x18\x03 \x01(\x0e\x32).opencensus.proto.trace.v1.Span.Link.Type\x12>\n\nattributes\x18\x04 \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.Attributes\x12>\n\ntracestate\x18\x05 \x01(\x0b\x32*.opencensus.proto.trace.v1.Span.Tracestate\"K\n\x04Type\x12\x14\n\x10TYPE_UNSPECIFIED\x10\x00\x12\x15\n\x11\x43HILD_LINKED_SPAN\x10\x01\x12\x16\n\x12PARENT_LINKED_SPAN\x10\x02\x1aX\n\x05Links\x12\x32\n\x04link\x18\x01 \x03(\x0b\x32$.opencensus.proto.trace.v1.Span.Link\x12\x1b\n\x13\x64ropped_links_count\x18\x02 \x01(\x05\"=\n\x08SpanKind\x12\x19\n\x15SPAN_KIND_UNSPECIFIED\x10\x00\x12\n\n\x06SERVER\x10\x01\x12\n\n\x06\x43LIENT\x10\x02\"\'\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t\"\xa2\x01\n\x0e\x41ttributeValue\x12\x44\n\x0cstring_value\x18\x01 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableStringH\x00\x12\x13\n\tint_value\x18\x02 \x01(\x03H\x00\x12\x14\n\nbool_value\x18\x03 \x01(\x08H\x00\x12\x16\n\x0c\x64ouble_value\x18\x04 \x01(\x01H\x00\x42\x07\n\x05value\"\xed\x04\n\nStackTrace\x12G\n\x0cstack_frames\x18\x01 \x01(\x0b\x32\x31.opencensus.proto.trace.v1.StackTrace.StackFrames\x12\x1b\n\x13stack_trace_hash_id\x18\x02 \x01(\x04\x1a\x8a\x03\n\nStackFrame\x12\x43\n\rfunction_name\x18\x01 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12L\n\x16original_function_name\x18\x02 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12?\n\tfile_name\x18\x03 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12\x13\n\x0bline_number\x18\x04 \x01(\x03\x12\x15\n\rcolumn_number\x18\x05 \x01(\x03\x12\x36\n\x0bload_module\x18\x06 \x01(\x0b\x32!.opencensus.proto.trace.v1.Module\x12\x44\n\x0esource_version\x18\x07 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x1al\n\x0bStackFrames\x12?\n\x05\x66rame\x18\x01 \x03(\x0b\x32\x30.opencensus.proto.trace.v1.StackTrace.StackFrame\x12\x1c\n\x14\x64ropped_frames_count\x18\x02 \x01(\x05\"\x86\x01\n\x06Module\x12<\n\x06module\x18\x01 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\x12>\n\x08\x62uild_id\x18\x02 \x01(\x0b\x32,.opencensus.proto.trace.v1.TruncatableString\"@\n\x11TruncatableString\x12\r\n\x05value\x18\x01 \x01(\t\x12\x1c\n\x14truncated_byte_count\x18\x02 \x01(\x05\x42\x8f\x01\n\x1cio.opencensus.proto.trace.v1B\nTraceProtoP\x01ZBgithub.com/census-instrumentation/opencensus-proto/gen-go/trace/v1\xea\x02\x1cOpenCensus::Proto::Trace::V1b\x06proto3')



_SPAN = DESCRIPTOR.message_types_by_name['Span']
_SPAN_TRACESTATE = _SPAN.nested_types_by_name['Tracestate']
_SPAN_TRACESTATE_ENTRY = _SPAN_TRACESTATE.nested_types_by_name['Entry']
_SPAN_ATTRIBUTES = _SPAN.nested_types_by_name['Attributes']
_SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY = _SPAN_ATTRIBUTES.nested_types_by_name['AttributeMapEntry']
_SPAN_TIMEEVENT = _SPAN.nested_types_by_name['TimeEvent']
_SPAN_TIMEEVENT_ANNOTATION = _SPAN_TIMEEVENT.nested_types_by_name['Annotation']
_SPAN_TIMEEVENT_MESSAGEEVENT = _SPAN_TIMEEVENT.nested_types_by_name['MessageEvent']
_SPAN_TIMEEVENTS = _SPAN.nested_types_by_name['TimeEvents']
_SPAN_LINK = _SPAN.nested_types_by_name['Link']
_SPAN_LINKS = _SPAN.nested_types_by_name['Links']
_STATUS = DESCRIPTOR.message_types_by_name['Status']
_ATTRIBUTEVALUE = DESCRIPTOR.message_types_by_name['AttributeValue']
_STACKTRACE = DESCRIPTOR.message_types_by_name['StackTrace']
_STACKTRACE_STACKFRAME = _STACKTRACE.nested_types_by_name['StackFrame']
_STACKTRACE_STACKFRAMES = _STACKTRACE.nested_types_by_name['StackFrames']
_MODULE = DESCRIPTOR.message_types_by_name['Module']
_TRUNCATABLESTRING = DESCRIPTOR.message_types_by_name['TruncatableString']
_SPAN_TIMEEVENT_MESSAGEEVENT_TYPE = _SPAN_TIMEEVENT_MESSAGEEVENT.enum_types_by_name['Type']
_SPAN_LINK_TYPE = _SPAN_LINK.enum_types_by_name['Type']
_SPAN_SPANKIND = _SPAN.enum_types_by_name['SpanKind']
Span = _reflection.GeneratedProtocolMessageType('Span', (_message.Message,), {

  'Tracestate' : _reflection.GeneratedProtocolMessageType('Tracestate', (_message.Message,), {

    'Entry' : _reflection.GeneratedProtocolMessageType('Entry', (_message.Message,), {
      'DESCRIPTOR' : _SPAN_TRACESTATE_ENTRY,
      '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
      # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Tracestate.Entry)
      })
    ,
    'DESCRIPTOR' : _SPAN_TRACESTATE,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Tracestate)
    })
  ,

  'Attributes' : _reflection.GeneratedProtocolMessageType('Attributes', (_message.Message,), {

    'AttributeMapEntry' : _reflection.GeneratedProtocolMessageType('AttributeMapEntry', (_message.Message,), {
      'DESCRIPTOR' : _SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY,
      '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
      # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Attributes.AttributeMapEntry)
      })
    ,
    'DESCRIPTOR' : _SPAN_ATTRIBUTES,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Attributes)
    })
  ,

  'TimeEvent' : _reflection.GeneratedProtocolMessageType('TimeEvent', (_message.Message,), {

    'Annotation' : _reflection.GeneratedProtocolMessageType('Annotation', (_message.Message,), {
      'DESCRIPTOR' : _SPAN_TIMEEVENT_ANNOTATION,
      '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
      # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.TimeEvent.Annotation)
      })
    ,

    'MessageEvent' : _reflection.GeneratedProtocolMessageType('MessageEvent', (_message.Message,), {
      'DESCRIPTOR' : _SPAN_TIMEEVENT_MESSAGEEVENT,
      '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
      # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.TimeEvent.MessageEvent)
      })
    ,
    'DESCRIPTOR' : _SPAN_TIMEEVENT,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.TimeEvent)
    })
  ,

  'TimeEvents' : _reflection.GeneratedProtocolMessageType('TimeEvents', (_message.Message,), {
    'DESCRIPTOR' : _SPAN_TIMEEVENTS,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.TimeEvents)
    })
  ,

  'Link' : _reflection.GeneratedProtocolMessageType('Link', (_message.Message,), {
    'DESCRIPTOR' : _SPAN_LINK,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Link)
    })
  ,

  'Links' : _reflection.GeneratedProtocolMessageType('Links', (_message.Message,), {
    'DESCRIPTOR' : _SPAN_LINKS,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span.Links)
    })
  ,
  'DESCRIPTOR' : _SPAN,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Span)
  })
_sym_db.RegisterMessage(Span)
_sym_db.RegisterMessage(Span.Tracestate)
_sym_db.RegisterMessage(Span.Tracestate.Entry)
_sym_db.RegisterMessage(Span.Attributes)
_sym_db.RegisterMessage(Span.Attributes.AttributeMapEntry)
_sym_db.RegisterMessage(Span.TimeEvent)
_sym_db.RegisterMessage(Span.TimeEvent.Annotation)
_sym_db.RegisterMessage(Span.TimeEvent.MessageEvent)
_sym_db.RegisterMessage(Span.TimeEvents)
_sym_db.RegisterMessage(Span.Link)
_sym_db.RegisterMessage(Span.Links)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), {
  'DESCRIPTOR' : _STATUS,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Status)
  })
_sym_db.RegisterMessage(Status)

AttributeValue = _reflection.GeneratedProtocolMessageType('AttributeValue', (_message.Message,), {
  'DESCRIPTOR' : _ATTRIBUTEVALUE,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.AttributeValue)
  })
_sym_db.RegisterMessage(AttributeValue)

StackTrace = _reflection.GeneratedProtocolMessageType('StackTrace', (_message.Message,), {

  'StackFrame' : _reflection.GeneratedProtocolMessageType('StackFrame', (_message.Message,), {
    'DESCRIPTOR' : _STACKTRACE_STACKFRAME,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.StackTrace.StackFrame)
    })
  ,

  'StackFrames' : _reflection.GeneratedProtocolMessageType('StackFrames', (_message.Message,), {
    'DESCRIPTOR' : _STACKTRACE_STACKFRAMES,
    '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
    # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.StackTrace.StackFrames)
    })
  ,
  'DESCRIPTOR' : _STACKTRACE,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.StackTrace)
  })
_sym_db.RegisterMessage(StackTrace)
_sym_db.RegisterMessage(StackTrace.StackFrame)
_sym_db.RegisterMessage(StackTrace.StackFrames)

Module = _reflection.GeneratedProtocolMessageType('Module', (_message.Message,), {
  'DESCRIPTOR' : _MODULE,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.Module)
  })
_sym_db.RegisterMessage(Module)

TruncatableString = _reflection.GeneratedProtocolMessageType('TruncatableString', (_message.Message,), {
  'DESCRIPTOR' : _TRUNCATABLESTRING,
  '__module__' : 'opencensus.proto.trace.v1.trace_pb2'
  # @@protoc_insertion_point(class_scope:opencensus.proto.trace.v1.TruncatableString)
  })
_sym_db.RegisterMessage(TruncatableString)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\034io.opencensus.proto.trace.v1B\nTraceProtoP\001ZBgithub.com/census-instrumentation/opencensus-proto/gen-go/trace/v1\352\002\034OpenCensus::Proto::Trace::V1'
  _SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY._options = None
  _SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY._serialized_options = b'8\001'
  _SPAN._serialized_start=179
  _SPAN._serialized_end=2527
  _SPAN_TRACESTATE._serialized_start=993
  _SPAN_TRACESTATE._serialized_end=1109
  _SPAN_TRACESTATE_ENTRY._serialized_start=1074
  _SPAN_TRACESTATE_ENTRY._serialized_end=1109
  _SPAN_ATTRIBUTES._serialized_start=1112
  _SPAN_ATTRIBUTES._serialized_end=1339
  _SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY._serialized_start=1245
  _SPAN_ATTRIBUTES_ATTRIBUTEMAPENTRY._serialized_end=1339
  _SPAN_TIMEEVENT._serialized_start=1342
  _SPAN_TIMEEVENT._serialized_end=1917
  _SPAN_TIMEEVENT_ANNOTATION._serialized_start=1555
  _SPAN_TIMEEVENT_ANNOTATION._serialized_end=1698
  _SPAN_TIMEEVENT_MESSAGEEVENT._serialized_start=1701
  _SPAN_TIMEEVENT_MESSAGEEVENT._serialized_end=1908
  _SPAN_TIMEEVENT_MESSAGEEVENT_TYPE._serialized_start=1856
  _SPAN_TIMEEVENT_MESSAGEEVENT_TYPE._serialized_end=1908
  _SPAN_TIMEEVENTS._serialized_start=1920
  _SPAN_TIMEEVENTS._serialized_end=2068
  _SPAN_LINK._serialized_start=2071
  _SPAN_LINK._serialized_end=2374
  _SPAN_LINK_TYPE._serialized_start=2299
  _SPAN_LINK_TYPE._serialized_end=2374
  _SPAN_LINKS._serialized_start=2376
  _SPAN_LINKS._serialized_end=2464
  _SPAN_SPANKIND._serialized_start=2466
  _SPAN_SPANKIND._serialized_end=2527
  _STATUS._serialized_start=2529
  _STATUS._serialized_end=2568
  _ATTRIBUTEVALUE._serialized_start=2571
  _ATTRIBUTEVALUE._serialized_end=2733
  _STACKTRACE._serialized_start=2736
  _STACKTRACE._serialized_end=3357
  _STACKTRACE_STACKFRAME._serialized_start=2853
  _STACKTRACE_STACKFRAME._serialized_end=3247
  _STACKTRACE_STACKFRAMES._serialized_start=3249
  _STACKTRACE_STACKFRAMES._serialized_end=3357
  _MODULE._serialized_start=3360
  _MODULE._serialized_end=3494
  _TRUNCATABLESTRING._serialized_start=3496
  _TRUNCATABLESTRING._serialized_end=3560
# @@protoc_insertion_point(module_scope)
