# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: users_list.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10users_list.proto\"\'\n\x05Users\x12\x0f\n\x07user_id\x18\x01 \x01(\t\x12\r\n\x05\x65mail\x18\x02 \x01(\t\"N\n\tPageUsers\x12\x0e\n\x06status\x18\x01 \x01(\t\x12\x18\n\x10total_count_page\x18\x02 \x01(\x05\x12\x17\n\x07results\x18\x03 \x03(\x0b\x32\x06.Users\"g\n\x0cUsersRequest\x12\x19\n\x11type_notification\x18\x01 \x01(\t\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x13\n\x0bpage_number\x18\x03 \x01(\x05\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x04 \x01(\t\"0\n\rUsersResponse\x12\x1f\n\x0busers_array\x18\x01 \x01(\x0b\x32\n.PageUsers27\n\nUsersArray\x12)\n\x08UserList\x12\r.UsersRequest\x1a\x0e.UsersResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'users_list_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _USERS._serialized_start=20
  _USERS._serialized_end=59
  _PAGEUSERS._serialized_start=61
  _PAGEUSERS._serialized_end=139
  _USERSREQUEST._serialized_start=141
  _USERSREQUEST._serialized_end=244
  _USERSRESPONSE._serialized_start=246
  _USERSRESPONSE._serialized_end=294
  _USERSARRAY._serialized_start=296
  _USERSARRAY._serialized_end=351
# @@protoc_insertion_point(module_scope)
