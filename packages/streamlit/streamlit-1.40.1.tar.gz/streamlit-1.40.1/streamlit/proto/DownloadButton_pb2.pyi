"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
*!
Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022-2024)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import builtins
import google.protobuf.descriptor
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class DownloadButton(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    LABEL_FIELD_NUMBER: builtins.int
    DEFAULT_FIELD_NUMBER: builtins.int
    HELP_FIELD_NUMBER: builtins.int
    FORM_ID_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    DISABLED_FIELD_NUMBER: builtins.int
    USE_CONTAINER_WIDTH_FIELD_NUMBER: builtins.int
    TYPE_FIELD_NUMBER: builtins.int
    ICON_FIELD_NUMBER: builtins.int
    id: builtins.str
    label: builtins.str
    default: builtins.bool
    help: builtins.str
    form_id: builtins.str
    url: builtins.str
    disabled: builtins.bool
    use_container_width: builtins.bool
    type: builtins.str
    icon: builtins.str
    def __init__(
        self,
        *,
        id: builtins.str = ...,
        label: builtins.str = ...,
        default: builtins.bool = ...,
        help: builtins.str = ...,
        form_id: builtins.str = ...,
        url: builtins.str = ...,
        disabled: builtins.bool = ...,
        use_container_width: builtins.bool = ...,
        type: builtins.str = ...,
        icon: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["default", b"default", "disabled", b"disabled", "form_id", b"form_id", "help", b"help", "icon", b"icon", "id", b"id", "label", b"label", "type", b"type", "url", b"url", "use_container_width", b"use_container_width"]) -> None: ...

global___DownloadButton = DownloadButton
