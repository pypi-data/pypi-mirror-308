# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: streamlit/proto/GitInfo.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1dstreamlit/proto/GitInfo.proto\"\xd6\x01\n\x07GitInfo\x12\x12\n\nrepository\x18\x01 \x01(\t\x12\x0e\n\x06\x62ranch\x18\x02 \x01(\t\x12\x0e\n\x06module\x18\x03 \x01(\t\x12\x17\n\x0funtracked_files\x18\x04 \x03(\t\x12\x19\n\x11uncommitted_files\x18\x05 \x03(\t\x12!\n\x05state\x18\x06 \x01(\x0e\x32\x12.GitInfo.GitStates\"@\n\tGitStates\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x11\n\rHEAD_DETACHED\x10\x01\x12\x13\n\x0f\x41HEAD_OF_REMOTE\x10\x02\x42,\n\x1c\x63om.snowflake.apps.streamlitB\x0cGitInfoProtob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'streamlit.proto.GitInfo_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  _globals['DESCRIPTOR']._loaded_options = None
  _globals['DESCRIPTOR']._serialized_options = b'\n\034com.snowflake.apps.streamlitB\014GitInfoProto'
  _globals['_GITINFO']._serialized_start=34
  _globals['_GITINFO']._serialized_end=248
  _globals['_GITINFO_GITSTATES']._serialized_start=184
  _globals['_GITINFO_GITSTATES']._serialized_end=248
# @@protoc_insertion_point(module_scope)
