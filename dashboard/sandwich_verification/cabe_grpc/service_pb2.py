# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import analysis_pb2 as analysis__pb2
import spec_pb2 as spec__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rservice.proto\x12\ncabe.proto\x1a\x0e\x61nalysis.proto\x1a\nspec.proto\"b\n\x12GetAnalysisRequest\x12\x17\n\x0fpinpoint_job_id\x18\x01 \x01(\t\x12\x33\n\x0f\x65xperiment_spec\x18\x02 \x01(\x0b\x32\x1a.cabe.proto.ExperimentSpec\"\x80\x01\n\x13GetAnalysisResponse\x12+\n\x07results\x18\x01 \x03(\x0b\x32\x1a.cabe.proto.AnalysisResult\x12<\n\x18inferred_experiment_spec\x18\x02 \x01(\x0b\x32\x1a.cabe.proto.ExperimentSpec2\\\n\x08\x41nalysis\x12P\n\x0bGetAnalysis\x12\x1e.cabe.proto.GetAnalysisRequest\x1a\x1f.cabe.proto.GetAnalysisResponse\"\x00\x42!Z\x1fgo.skia.org/infra/cabe/go/protob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'service_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z\037go.skia.org/infra/cabe/go/proto'
  _globals['_GETANALYSISREQUEST']._serialized_start=57
  _globals['_GETANALYSISREQUEST']._serialized_end=155
  _globals['_GETANALYSISRESPONSE']._serialized_start=158
  _globals['_GETANALYSISRESPONSE']._serialized_end=286
  _globals['_ANALYSIS']._serialized_start=288
  _globals['_ANALYSIS']._serialized_end=380
# @@protoc_insertion_point(module_scope)
