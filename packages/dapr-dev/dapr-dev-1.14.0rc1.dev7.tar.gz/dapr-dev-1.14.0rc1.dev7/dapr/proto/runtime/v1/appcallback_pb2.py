# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: dapr/proto/runtime/v1/appcallback.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import any_pb2 as google_dot_protobuf_dot_any__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from dapr.proto.common.v1 import common_pb2 as dapr_dot_proto_dot_common_dot_v1_dot_common__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\'dapr/proto/runtime/v1/appcallback.proto\x12\x15\x64\x61pr.proto.runtime.v1\x1a\x19google/protobuf/any.proto\x1a\x1bgoogle/protobuf/empty.proto\x1a!dapr/proto/common/v1/common.proto\x1a\x1cgoogle/protobuf/struct.proto\"\xa6\x01\n\x0fJobEventRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\"\n\x04\x64\x61ta\x18\x02 \x01(\x0b\x32\x14.google.protobuf.Any\x12\x0e\n\x06method\x18\x03 \x01(\t\x12\x14\n\x0c\x63ontent_type\x18\x04 \x01(\t\x12;\n\x0ehttp_extension\x18\x05 \x01(\x0b\x32#.dapr.proto.common.v1.HTTPExtension\"\x12\n\x10JobEventResponse\"\xdb\x01\n\x11TopicEventRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06source\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x14\n\x0cspec_version\x18\x04 \x01(\t\x12\x19\n\x11\x64\x61ta_content_type\x18\x05 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x07 \x01(\x0c\x12\r\n\x05topic\x18\x06 \x01(\t\x12\x13\n\x0bpubsub_name\x18\x08 \x01(\t\x12\x0c\n\x04path\x18\t \x01(\t\x12+\n\nextensions\x18\n \x01(\x0b\x32\x17.google.protobuf.Struct\"\xa6\x01\n\x12TopicEventResponse\x12R\n\x06status\x18\x01 \x01(\x0e\x32\x42.dapr.proto.runtime.v1.TopicEventResponse.TopicEventResponseStatus\"<\n\x18TopicEventResponseStatus\x12\x0b\n\x07SUCCESS\x10\x00\x12\t\n\x05RETRY\x10\x01\x12\x08\n\x04\x44ROP\x10\x02\"\xab\x01\n\x13TopicEventCERequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0e\n\x06source\x18\x02 \x01(\t\x12\x0c\n\x04type\x18\x03 \x01(\t\x12\x14\n\x0cspec_version\x18\x04 \x01(\t\x12\x19\n\x11\x64\x61ta_content_type\x18\x05 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x06 \x01(\x0c\x12+\n\nextensions\x18\x07 \x01(\x0b\x32\x17.google.protobuf.Struct\"\xa5\x02\n\x1aTopicEventBulkRequestEntry\x12\x10\n\x08\x65ntry_id\x18\x01 \x01(\t\x12\x0f\n\x05\x62ytes\x18\x02 \x01(\x0cH\x00\x12\x41\n\x0b\x63loud_event\x18\x03 \x01(\x0b\x32*.dapr.proto.runtime.v1.TopicEventCERequestH\x00\x12\x14\n\x0c\x63ontent_type\x18\x04 \x01(\t\x12Q\n\x08metadata\x18\x05 \x03(\x0b\x32?.dapr.proto.runtime.v1.TopicEventBulkRequestEntry.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x07\n\x05\x65vent\"\xa6\x02\n\x15TopicEventBulkRequest\x12\n\n\x02id\x18\x01 \x01(\t\x12\x42\n\x07\x65ntries\x18\x02 \x03(\x0b\x32\x31.dapr.proto.runtime.v1.TopicEventBulkRequestEntry\x12L\n\x08metadata\x18\x03 \x03(\x0b\x32:.dapr.proto.runtime.v1.TopicEventBulkRequest.MetadataEntry\x12\r\n\x05topic\x18\x04 \x01(\t\x12\x13\n\x0bpubsub_name\x18\x05 \x01(\t\x12\x0c\n\x04type\x18\x06 \x01(\t\x12\x0c\n\x04path\x18\x07 \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x83\x01\n\x1bTopicEventBulkResponseEntry\x12\x10\n\x08\x65ntry_id\x18\x01 \x01(\t\x12R\n\x06status\x18\x02 \x01(\x0e\x32\x42.dapr.proto.runtime.v1.TopicEventResponse.TopicEventResponseStatus\"^\n\x16TopicEventBulkResponse\x12\x44\n\x08statuses\x18\x01 \x03(\x0b\x32\x32.dapr.proto.runtime.v1.TopicEventBulkResponseEntry\"\xae\x01\n\x13\x42indingEventRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\x0c\x12J\n\x08metadata\x18\x03 \x03(\x0b\x32\x38.dapr.proto.runtime.v1.BindingEventRequest.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x88\x02\n\x14\x42indingEventResponse\x12\x12\n\nstore_name\x18\x01 \x01(\t\x12/\n\x06states\x18\x02 \x03(\x0b\x32\x1f.dapr.proto.common.v1.StateItem\x12\n\n\x02to\x18\x03 \x03(\t\x12\x0c\n\x04\x64\x61ta\x18\x04 \x01(\x0c\x12X\n\x0b\x63oncurrency\x18\x05 \x01(\x0e\x32\x43.dapr.proto.runtime.v1.BindingEventResponse.BindingEventConcurrency\"7\n\x17\x42indingEventConcurrency\x12\x0e\n\nSEQUENTIAL\x10\x00\x12\x0c\n\x08PARALLEL\x10\x01\"a\n\x1eListTopicSubscriptionsResponse\x12?\n\rsubscriptions\x18\x01 \x03(\x0b\x32(.dapr.proto.runtime.v1.TopicSubscription\"\xc5\x02\n\x11TopicSubscription\x12\x13\n\x0bpubsub_name\x18\x01 \x01(\t\x12\r\n\x05topic\x18\x02 \x01(\t\x12H\n\x08metadata\x18\x03 \x03(\x0b\x32\x36.dapr.proto.runtime.v1.TopicSubscription.MetadataEntry\x12\x32\n\x06routes\x18\x05 \x01(\x0b\x32\".dapr.proto.runtime.v1.TopicRoutes\x12\x19\n\x11\x64\x65\x61\x64_letter_topic\x18\x06 \x01(\t\x12\x42\n\x0e\x62ulk_subscribe\x18\x07 \x01(\x0b\x32*.dapr.proto.runtime.v1.BulkSubscribeConfig\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"O\n\x0bTopicRoutes\x12/\n\x05rules\x18\x01 \x03(\x0b\x32 .dapr.proto.runtime.v1.TopicRule\x12\x0f\n\x07\x64\x65\x66\x61ult\x18\x02 \x01(\t\"(\n\tTopicRule\x12\r\n\x05match\x18\x01 \x01(\t\x12\x0c\n\x04path\x18\x02 \x01(\t\"a\n\x13\x42ulkSubscribeConfig\x12\x0f\n\x07\x65nabled\x18\x01 \x01(\x08\x12\x1a\n\x12max_messages_count\x18\x02 \x01(\x05\x12\x1d\n\x15max_await_duration_ms\x18\x03 \x01(\x05\"-\n\x19ListInputBindingsResponse\x12\x10\n\x08\x62indings\x18\x01 \x03(\t\"\x15\n\x13HealthCheckResponse2\x86\x04\n\x0b\x41ppCallback\x12W\n\x08OnInvoke\x12#.dapr.proto.common.v1.InvokeRequest\x1a$.dapr.proto.common.v1.InvokeResponse\"\x00\x12i\n\x16ListTopicSubscriptions\x12\x16.google.protobuf.Empty\x1a\x35.dapr.proto.runtime.v1.ListTopicSubscriptionsResponse\"\x00\x12\x65\n\x0cOnTopicEvent\x12(.dapr.proto.runtime.v1.TopicEventRequest\x1a).dapr.proto.runtime.v1.TopicEventResponse\"\x00\x12_\n\x11ListInputBindings\x12\x16.google.protobuf.Empty\x1a\x30.dapr.proto.runtime.v1.ListInputBindingsResponse\"\x00\x12k\n\x0eOnBindingEvent\x12*.dapr.proto.runtime.v1.BindingEventRequest\x1a+.dapr.proto.runtime.v1.BindingEventResponse\"\x00\x32m\n\x16\x41ppCallbackHealthCheck\x12S\n\x0bHealthCheck\x12\x16.google.protobuf.Empty\x1a*.dapr.proto.runtime.v1.HealthCheckResponse\"\x00\x32\xf0\x01\n\x10\x41ppCallbackAlpha\x12w\n\x16OnBulkTopicEventAlpha1\x12,.dapr.proto.runtime.v1.TopicEventBulkRequest\x1a-.dapr.proto.runtime.v1.TopicEventBulkResponse\"\x00\x12\x63\n\x10OnJobEventAlpha1\x12&.dapr.proto.runtime.v1.JobEventRequest\x1a\'.dapr.proto.runtime.v1.JobEventResponseBy\n\nio.dapr.v1B\x15\x44\x61prAppCallbackProtosZ1github.com/dapr/dapr/pkg/proto/runtime/v1;runtime\xaa\x02 Dapr.AppCallback.Autogen.Grpc.v1b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'dapr.proto.runtime.v1.appcallback_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\nio.dapr.v1B\025DaprAppCallbackProtosZ1github.com/dapr/dapr/pkg/proto/runtime/v1;runtime\252\002 Dapr.AppCallback.Autogen.Grpc.v1'
  _TOPICEVENTBULKREQUESTENTRY_METADATAENTRY._options = None
  _TOPICEVENTBULKREQUESTENTRY_METADATAENTRY._serialized_options = b'8\001'
  _TOPICEVENTBULKREQUEST_METADATAENTRY._options = None
  _TOPICEVENTBULKREQUEST_METADATAENTRY._serialized_options = b'8\001'
  _BINDINGEVENTREQUEST_METADATAENTRY._options = None
  _BINDINGEVENTREQUEST_METADATAENTRY._serialized_options = b'8\001'
  _TOPICSUBSCRIPTION_METADATAENTRY._options = None
  _TOPICSUBSCRIPTION_METADATAENTRY._serialized_options = b'8\001'
  _globals['_JOBEVENTREQUEST']._serialized_start=188
  _globals['_JOBEVENTREQUEST']._serialized_end=354
  _globals['_JOBEVENTRESPONSE']._serialized_start=356
  _globals['_JOBEVENTRESPONSE']._serialized_end=374
  _globals['_TOPICEVENTREQUEST']._serialized_start=377
  _globals['_TOPICEVENTREQUEST']._serialized_end=596
  _globals['_TOPICEVENTRESPONSE']._serialized_start=599
  _globals['_TOPICEVENTRESPONSE']._serialized_end=765
  _globals['_TOPICEVENTRESPONSE_TOPICEVENTRESPONSESTATUS']._serialized_start=705
  _globals['_TOPICEVENTRESPONSE_TOPICEVENTRESPONSESTATUS']._serialized_end=765
  _globals['_TOPICEVENTCEREQUEST']._serialized_start=768
  _globals['_TOPICEVENTCEREQUEST']._serialized_end=939
  _globals['_TOPICEVENTBULKREQUESTENTRY']._serialized_start=942
  _globals['_TOPICEVENTBULKREQUESTENTRY']._serialized_end=1235
  _globals['_TOPICEVENTBULKREQUESTENTRY_METADATAENTRY']._serialized_start=1179
  _globals['_TOPICEVENTBULKREQUESTENTRY_METADATAENTRY']._serialized_end=1226
  _globals['_TOPICEVENTBULKREQUEST']._serialized_start=1238
  _globals['_TOPICEVENTBULKREQUEST']._serialized_end=1532
  _globals['_TOPICEVENTBULKREQUEST_METADATAENTRY']._serialized_start=1179
  _globals['_TOPICEVENTBULKREQUEST_METADATAENTRY']._serialized_end=1226
  _globals['_TOPICEVENTBULKRESPONSEENTRY']._serialized_start=1535
  _globals['_TOPICEVENTBULKRESPONSEENTRY']._serialized_end=1666
  _globals['_TOPICEVENTBULKRESPONSE']._serialized_start=1668
  _globals['_TOPICEVENTBULKRESPONSE']._serialized_end=1762
  _globals['_BINDINGEVENTREQUEST']._serialized_start=1765
  _globals['_BINDINGEVENTREQUEST']._serialized_end=1939
  _globals['_BINDINGEVENTREQUEST_METADATAENTRY']._serialized_start=1179
  _globals['_BINDINGEVENTREQUEST_METADATAENTRY']._serialized_end=1226
  _globals['_BINDINGEVENTRESPONSE']._serialized_start=1942
  _globals['_BINDINGEVENTRESPONSE']._serialized_end=2206
  _globals['_BINDINGEVENTRESPONSE_BINDINGEVENTCONCURRENCY']._serialized_start=2151
  _globals['_BINDINGEVENTRESPONSE_BINDINGEVENTCONCURRENCY']._serialized_end=2206
  _globals['_LISTTOPICSUBSCRIPTIONSRESPONSE']._serialized_start=2208
  _globals['_LISTTOPICSUBSCRIPTIONSRESPONSE']._serialized_end=2305
  _globals['_TOPICSUBSCRIPTION']._serialized_start=2308
  _globals['_TOPICSUBSCRIPTION']._serialized_end=2633
  _globals['_TOPICSUBSCRIPTION_METADATAENTRY']._serialized_start=1179
  _globals['_TOPICSUBSCRIPTION_METADATAENTRY']._serialized_end=1226
  _globals['_TOPICROUTES']._serialized_start=2635
  _globals['_TOPICROUTES']._serialized_end=2714
  _globals['_TOPICRULE']._serialized_start=2716
  _globals['_TOPICRULE']._serialized_end=2756
  _globals['_BULKSUBSCRIBECONFIG']._serialized_start=2758
  _globals['_BULKSUBSCRIBECONFIG']._serialized_end=2855
  _globals['_LISTINPUTBINDINGSRESPONSE']._serialized_start=2857
  _globals['_LISTINPUTBINDINGSRESPONSE']._serialized_end=2902
  _globals['_HEALTHCHECKRESPONSE']._serialized_start=2904
  _globals['_HEALTHCHECKRESPONSE']._serialized_end=2925
  _globals['_APPCALLBACK']._serialized_start=2928
  _globals['_APPCALLBACK']._serialized_end=3446
  _globals['_APPCALLBACKHEALTHCHECK']._serialized_start=3448
  _globals['_APPCALLBACKHEALTHCHECK']._serialized_end=3557
  _globals['_APPCALLBACKALPHA']._serialized_start=3560
  _globals['_APPCALLBACKALPHA']._serialized_end=3800
# @@protoc_insertion_point(module_scope)
