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
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import typing

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

@typing.final
class ComponentInstance(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ID_FIELD_NUMBER: builtins.int
    JSON_ARGS_FIELD_NUMBER: builtins.int
    SPECIAL_ARGS_FIELD_NUMBER: builtins.int
    COMPONENT_NAME_FIELD_NUMBER: builtins.int
    URL_FIELD_NUMBER: builtins.int
    FORM_ID_FIELD_NUMBER: builtins.int
    id: builtins.str
    """The instance's "widget ID", used to uniquely identify it."""
    json_args: builtins.str
    """Argument dictionary, for JSON-serializable args."""
    component_name: builtins.str
    """The component type's unique name."""
    url: builtins.str
    """Optional URL to load the component from. By default this is not set,
    but while testing, a user can e.g. point this to a local node server
    that they're developing their component in.
    """
    form_id: builtins.str
    @property
    def special_args(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___SpecialArg]:
        """Additional, non-JSON args. These require special processing
        on the other end.
        """

    def __init__(
        self,
        *,
        id: builtins.str = ...,
        json_args: builtins.str = ...,
        special_args: collections.abc.Iterable[global___SpecialArg] | None = ...,
        component_name: builtins.str = ...,
        url: builtins.str = ...,
        form_id: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["component_name", b"component_name", "form_id", b"form_id", "id", b"id", "json_args", b"json_args", "special_args", b"special_args", "url", b"url"]) -> None: ...

global___ComponentInstance = ComponentInstance

@typing.final
class SpecialArg(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    KEY_FIELD_NUMBER: builtins.int
    ARROW_DATAFRAME_FIELD_NUMBER: builtins.int
    BYTES_FIELD_NUMBER: builtins.int
    key: builtins.str
    bytes: builtins.bytes
    @property
    def arrow_dataframe(self) -> global___ArrowDataframe: ...
    def __init__(
        self,
        *,
        key: builtins.str = ...,
        arrow_dataframe: global___ArrowDataframe | None = ...,
        bytes: builtins.bytes = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["arrow_dataframe", b"arrow_dataframe", "bytes", b"bytes", "value", b"value"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["arrow_dataframe", b"arrow_dataframe", "bytes", b"bytes", "key", b"key", "value", b"value"]) -> None: ...
    def WhichOneof(self, oneof_group: typing.Literal["value", b"value"]) -> typing.Literal["arrow_dataframe", "bytes"] | None: ...

global___SpecialArg = SpecialArg

@typing.final
class ArrowDataframe(google.protobuf.message.Message):
    """Components uses Apache Arrow for dataframe serialization.
    This is distinct from `Arrow.proto`: Components was created before
    Streamlit supported Arrow for internal dataframe serialization, and the
    two implementations currently use different logic + data structures.
    """

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    HEIGHT_FIELD_NUMBER: builtins.int
    WIDTH_FIELD_NUMBER: builtins.int
    height: builtins.int
    width: builtins.int
    @property
    def data(self) -> global___ArrowTable: ...
    def __init__(
        self,
        *,
        data: global___ArrowTable | None = ...,
        height: builtins.int = ...,
        width: builtins.int = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["data", b"data"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["data", b"data", "height", b"height", "width", b"width"]) -> None: ...

global___ArrowDataframe = ArrowDataframe

@typing.final
class ArrowTable(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    INDEX_FIELD_NUMBER: builtins.int
    COLUMNS_FIELD_NUMBER: builtins.int
    STYLER_FIELD_NUMBER: builtins.int
    data: builtins.bytes
    index: builtins.bytes
    columns: builtins.bytes
    @property
    def styler(self) -> global___ArrowTableStyler: ...
    def __init__(
        self,
        *,
        data: builtins.bytes = ...,
        index: builtins.bytes = ...,
        columns: builtins.bytes = ...,
        styler: global___ArrowTableStyler | None = ...,
    ) -> None: ...
    def HasField(self, field_name: typing.Literal["styler", b"styler"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing.Literal["columns", b"columns", "data", b"data", "index", b"index", "styler", b"styler"]) -> None: ...

global___ArrowTable = ArrowTable

@typing.final
class ArrowTableStyler(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    UUID_FIELD_NUMBER: builtins.int
    CAPTION_FIELD_NUMBER: builtins.int
    STYLES_FIELD_NUMBER: builtins.int
    DISPLAY_VALUES_FIELD_NUMBER: builtins.int
    uuid: builtins.str
    caption: builtins.str
    styles: builtins.str
    display_values: builtins.bytes
    def __init__(
        self,
        *,
        uuid: builtins.str = ...,
        caption: builtins.str = ...,
        styles: builtins.str = ...,
        display_values: builtins.bytes = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing.Literal["caption", b"caption", "display_values", b"display_values", "styles", b"styles", "uuid", b"uuid"]) -> None: ...

global___ArrowTableStyler = ArrowTableStyler
