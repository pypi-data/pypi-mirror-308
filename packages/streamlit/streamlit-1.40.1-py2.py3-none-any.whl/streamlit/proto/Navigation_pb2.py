# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streamlit/proto/Navigation.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from streamlit.proto import AppPage_pb2 as streamlit_dot_proto_dot_AppPage__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n streamlit/proto/Navigation.proto\x1a\x1dstreamlit/proto/AppPage.proto\"\xb4\x01\n\nNavigation\x12\x10\n\x08sections\x18\x01 \x03(\t\x12\x1b\n\tapp_pages\x18\x02 \x03(\x0b\x32\x08.AppPage\x12&\n\x08position\x18\x03 \x01(\x0e\x32\x14.Navigation.Position\x12\x18\n\x10page_script_hash\x18\x04 \x01(\t\x12\x10\n\x08\x65xpanded\x18\x05 \x01(\x08\"#\n\x08Position\x12\n\n\x06HIDDEN\x10\x00\x12\x0b\n\x07SIDEBAR\x10\x01\x42\x1e\n\x1c\x63om.snowflake.apps.streamlitb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'streamlit.proto.Navigation_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.snowflake.apps.streamlit'
  _globals['_NAVIGATION']._serialized_start=68
  _globals['_NAVIGATION']._serialized_end=248
  _globals['_NAVIGATION_POSITION']._serialized_start=213
  _globals['_NAVIGATION_POSITION']._serialized_end=248
# @@protoc_insertion_point(module_scope)
