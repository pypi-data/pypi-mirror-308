# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/server/v1/bootstrap.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""

from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.server.v1 import environment_pb2 as chalk_dot_server_dot_v1_dot_environment__pb2
from chalk._gen.chalk.server.v1 import team_pb2 as chalk_dot_server_dot_v1_dot_team__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1f\x63halk/server/v1/bootstrap.proto\x12\x0f\x63halk.server.v1\x1a!chalk/server/v1/environment.proto\x1a\x1a\x63halk/server/v1/team.proto"\xbe\x01\n!BootstrapExtraSettingsEnvironment\x12\\\n\x08settings\x18\x01 \x03(\x0b\x32@.chalk.server.v1.BootstrapExtraSettingsEnvironment.SettingsEntryR\x08settings\x1a;\n\rSettingsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x08R\x05value:\x02\x38\x01"\xf4\x02\n\x16\x42ootstrapExtraSettings\x12K\n\x06global\x18\x01 \x03(\x0b\x32\x33.chalk.server.v1.BootstrapExtraSettings.GlobalEntryR\x06global\x12]\n\x0c\x65nvironments\x18\x02 \x03(\x0b\x32\x39.chalk.server.v1.BootstrapExtraSettings.EnvironmentsEntryR\x0c\x65nvironments\x1a\x39\n\x0bGlobalEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x14\n\x05value\x18\x02 \x01(\x08R\x05value:\x02\x38\x01\x1as\n\x11\x45nvironmentsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12H\n\x05value\x18\x02 \x01(\x0b\x32\x32.chalk.server.v1.BootstrapExtraSettingsEnvironmentR\x05value:\x02\x38\x01"\xcd\x02\n\x16ParsedBootstrapConfigs\x12+\n\x05teams\x18\x01 \x03(\x0b\x32\x15.chalk.server.v1.TeamR\x05teams\x12\x34\n\x08projects\x18\x02 \x03(\x0b\x32\x18.chalk.server.v1.ProjectR\x08projects\x12@\n\x0c\x65nvironments\x18\x03 \x03(\x0b\x32\x1c.chalk.server.v1.EnvironmentR\x0c\x65nvironments\x12>\n\x0cteam_invites\x18\x04 \x03(\x0b\x32\x1b.chalk.server.v1.TeamInviteR\x0bteamInvites\x12N\n\x0e\x65xtra_settings\x18\x05 \x01(\x0b\x32\'.chalk.server.v1.BootstrapExtraSettingsR\rextraSettingsB\x97\x01\n\x13\x63om.chalk.server.v1B\x0e\x42ootstrapProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43SX\xaa\x02\x0f\x43halk.Server.V1\xca\x02\x0f\x43halk\\Server\\V1\xe2\x02\x1b\x43halk\\Server\\V1\\GPBMetadata\xea\x02\x11\x43halk::Server::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.server.v1.bootstrap_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.server.v1B\016BootstrapProtoP\001Z\022server/v1;serverv1\242\002\003CSX\252\002\017Chalk.Server.V1\312\002\017Chalk\\Server\\V1\342\002\033Chalk\\Server\\V1\\GPBMetadata\352\002\021Chalk::Server::V1"
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT_SETTINGSENTRY"]._options = None
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT_SETTINGSENTRY"]._serialized_options = b"8\001"
    _globals["_BOOTSTRAPEXTRASETTINGS_GLOBALENTRY"]._options = None
    _globals["_BOOTSTRAPEXTRASETTINGS_GLOBALENTRY"]._serialized_options = b"8\001"
    _globals["_BOOTSTRAPEXTRASETTINGS_ENVIRONMENTSENTRY"]._options = None
    _globals["_BOOTSTRAPEXTRASETTINGS_ENVIRONMENTSENTRY"]._serialized_options = b"8\001"
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT"]._serialized_start = 116
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT"]._serialized_end = 306
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT_SETTINGSENTRY"]._serialized_start = 247
    _globals["_BOOTSTRAPEXTRASETTINGSENVIRONMENT_SETTINGSENTRY"]._serialized_end = 306
    _globals["_BOOTSTRAPEXTRASETTINGS"]._serialized_start = 309
    _globals["_BOOTSTRAPEXTRASETTINGS"]._serialized_end = 681
    _globals["_BOOTSTRAPEXTRASETTINGS_GLOBALENTRY"]._serialized_start = 507
    _globals["_BOOTSTRAPEXTRASETTINGS_GLOBALENTRY"]._serialized_end = 564
    _globals["_BOOTSTRAPEXTRASETTINGS_ENVIRONMENTSENTRY"]._serialized_start = 566
    _globals["_BOOTSTRAPEXTRASETTINGS_ENVIRONMENTSENTRY"]._serialized_end = 681
    _globals["_PARSEDBOOTSTRAPCONFIGS"]._serialized_start = 684
    _globals["_PARSEDBOOTSTRAPCONFIGS"]._serialized_end = 1017
# @@protoc_insertion_point(module_scope)
