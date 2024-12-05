"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import google.api.launch_stage_pb2
import google.protobuf.descriptor
import google.protobuf.descriptor_pb2
import google.protobuf.duration_pb2
import google.protobuf.internal.containers
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.internal.extension_dict
import google.protobuf.message
import typing
import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor = ...

class _ClientLibraryOrganization:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ClientLibraryOrganizationEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ClientLibraryOrganization.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    CLIENT_LIBRARY_ORGANIZATION_UNSPECIFIED: ClientLibraryOrganization.ValueType = ...  # 0
    """Not useful."""

    CLOUD: ClientLibraryOrganization.ValueType = ...  # 1
    """Google Cloud Platform Org."""

    ADS: ClientLibraryOrganization.ValueType = ...  # 2
    """Ads (Advertising) Org."""

    PHOTOS: ClientLibraryOrganization.ValueType = ...  # 3
    """Photos Org."""

    STREET_VIEW: ClientLibraryOrganization.ValueType = ...  # 4
    """Street View Org."""

    SHOPPING: ClientLibraryOrganization.ValueType = ...  # 5
    """Shopping Org."""

    GEO: ClientLibraryOrganization.ValueType = ...  # 6
    """Geo Org."""

    GENERATIVE_AI: ClientLibraryOrganization.ValueType = ...  # 7
    """Generative AI - https://developers.generativeai.google"""

class ClientLibraryOrganization(_ClientLibraryOrganization, metaclass=_ClientLibraryOrganizationEnumTypeWrapper):
    """The organization for which the client libraries are being published.
    Affects the url where generated docs are published, etc.
    """
    pass

CLIENT_LIBRARY_ORGANIZATION_UNSPECIFIED: ClientLibraryOrganization.ValueType = ...  # 0
"""Not useful."""

CLOUD: ClientLibraryOrganization.ValueType = ...  # 1
"""Google Cloud Platform Org."""

ADS: ClientLibraryOrganization.ValueType = ...  # 2
"""Ads (Advertising) Org."""

PHOTOS: ClientLibraryOrganization.ValueType = ...  # 3
"""Photos Org."""

STREET_VIEW: ClientLibraryOrganization.ValueType = ...  # 4
"""Street View Org."""

SHOPPING: ClientLibraryOrganization.ValueType = ...  # 5
"""Shopping Org."""

GEO: ClientLibraryOrganization.ValueType = ...  # 6
"""Geo Org."""

GENERATIVE_AI: ClientLibraryOrganization.ValueType = ...  # 7
"""Generative AI - https://developers.generativeai.google"""

global___ClientLibraryOrganization = ClientLibraryOrganization


class _ClientLibraryDestination:
    ValueType = typing.NewType('ValueType', builtins.int)
    V: typing_extensions.TypeAlias = ValueType
class _ClientLibraryDestinationEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_ClientLibraryDestination.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor = ...
    CLIENT_LIBRARY_DESTINATION_UNSPECIFIED: ClientLibraryDestination.ValueType = ...  # 0
    """Client libraries will neither be generated nor published to package
    managers.
    """

    GITHUB: ClientLibraryDestination.ValueType = ...  # 10
    """Generate the client library in a repo under github.com/googleapis,
    but don't publish it to package managers.
    """

    PACKAGE_MANAGER: ClientLibraryDestination.ValueType = ...  # 20
    """Publish the library to package managers like nuget.org and npmjs.com."""

class ClientLibraryDestination(_ClientLibraryDestination, metaclass=_ClientLibraryDestinationEnumTypeWrapper):
    """To where should client libraries be published?"""
    pass

CLIENT_LIBRARY_DESTINATION_UNSPECIFIED: ClientLibraryDestination.ValueType = ...  # 0
"""Client libraries will neither be generated nor published to package
managers.
"""

GITHUB: ClientLibraryDestination.ValueType = ...  # 10
"""Generate the client library in a repo under github.com/googleapis,
but don't publish it to package managers.
"""

PACKAGE_MANAGER: ClientLibraryDestination.ValueType = ...  # 20
"""Publish the library to package managers like nuget.org and npmjs.com."""

global___ClientLibraryDestination = ClientLibraryDestination


class CommonLanguageSettings(google.protobuf.message.Message):
    """Required information for every language."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    REFERENCE_DOCS_URI_FIELD_NUMBER: builtins.int
    DESTINATIONS_FIELD_NUMBER: builtins.int
    reference_docs_uri: typing.Text = ...
    """Link to automatically generated reference documentation.  Example:
    https://cloud.google.com/nodejs/docs/reference/asset/latest
    """

    @property
    def destinations(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[global___ClientLibraryDestination.ValueType]:
        """The destination where API teams want this client library to be published."""
        pass
    def __init__(self,
        *,
        reference_docs_uri : typing.Text = ...,
        destinations : typing.Optional[typing.Iterable[global___ClientLibraryDestination.ValueType]] = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["destinations",b"destinations","reference_docs_uri",b"reference_docs_uri"]) -> None: ...
global___CommonLanguageSettings = CommonLanguageSettings

class ClientLibrarySettings(google.protobuf.message.Message):
    """Details about how and where to publish client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    VERSION_FIELD_NUMBER: builtins.int
    LAUNCH_STAGE_FIELD_NUMBER: builtins.int
    REST_NUMERIC_ENUMS_FIELD_NUMBER: builtins.int
    JAVA_SETTINGS_FIELD_NUMBER: builtins.int
    CPP_SETTINGS_FIELD_NUMBER: builtins.int
    PHP_SETTINGS_FIELD_NUMBER: builtins.int
    PYTHON_SETTINGS_FIELD_NUMBER: builtins.int
    NODE_SETTINGS_FIELD_NUMBER: builtins.int
    DOTNET_SETTINGS_FIELD_NUMBER: builtins.int
    RUBY_SETTINGS_FIELD_NUMBER: builtins.int
    GO_SETTINGS_FIELD_NUMBER: builtins.int
    version: typing.Text = ...
    """Version of the API to apply these settings to. This is the full protobuf
    package for the API, ending in the version element.
    Examples: "google.cloud.speech.v1" and "google.spanner.admin.database.v1".
    """

    launch_stage: google.api.launch_stage_pb2.LaunchStage.ValueType = ...
    """Launch stage of this version of the API."""

    rest_numeric_enums: builtins.bool = ...
    """When using transport=rest, the client request will encode enums as
    numbers rather than strings.
    """

    @property
    def java_settings(self) -> global___JavaSettings:
        """Settings for legacy Java features, supported in the Service YAML."""
        pass
    @property
    def cpp_settings(self) -> global___CppSettings:
        """Settings for C++ client libraries."""
        pass
    @property
    def php_settings(self) -> global___PhpSettings:
        """Settings for PHP client libraries."""
        pass
    @property
    def python_settings(self) -> global___PythonSettings:
        """Settings for Python client libraries."""
        pass
    @property
    def node_settings(self) -> global___NodeSettings:
        """Settings for Node client libraries."""
        pass
    @property
    def dotnet_settings(self) -> global___DotnetSettings:
        """Settings for .NET client libraries."""
        pass
    @property
    def ruby_settings(self) -> global___RubySettings:
        """Settings for Ruby client libraries."""
        pass
    @property
    def go_settings(self) -> global___GoSettings:
        """Settings for Go client libraries."""
        pass
    def __init__(self,
        *,
        version : typing.Text = ...,
        launch_stage : google.api.launch_stage_pb2.LaunchStage.ValueType = ...,
        rest_numeric_enums : builtins.bool = ...,
        java_settings : typing.Optional[global___JavaSettings] = ...,
        cpp_settings : typing.Optional[global___CppSettings] = ...,
        php_settings : typing.Optional[global___PhpSettings] = ...,
        python_settings : typing.Optional[global___PythonSettings] = ...,
        node_settings : typing.Optional[global___NodeSettings] = ...,
        dotnet_settings : typing.Optional[global___DotnetSettings] = ...,
        ruby_settings : typing.Optional[global___RubySettings] = ...,
        go_settings : typing.Optional[global___GoSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["cpp_settings",b"cpp_settings","dotnet_settings",b"dotnet_settings","go_settings",b"go_settings","java_settings",b"java_settings","node_settings",b"node_settings","php_settings",b"php_settings","python_settings",b"python_settings","ruby_settings",b"ruby_settings"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["cpp_settings",b"cpp_settings","dotnet_settings",b"dotnet_settings","go_settings",b"go_settings","java_settings",b"java_settings","launch_stage",b"launch_stage","node_settings",b"node_settings","php_settings",b"php_settings","python_settings",b"python_settings","rest_numeric_enums",b"rest_numeric_enums","ruby_settings",b"ruby_settings","version",b"version"]) -> None: ...
global___ClientLibrarySettings = ClientLibrarySettings

class Publishing(google.protobuf.message.Message):
    """This message configures the settings for publishing [Google Cloud Client
    libraries](https://cloud.google.com/apis/docs/cloud-client-libraries)
    generated from the service config.
    """
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    METHOD_SETTINGS_FIELD_NUMBER: builtins.int
    NEW_ISSUE_URI_FIELD_NUMBER: builtins.int
    DOCUMENTATION_URI_FIELD_NUMBER: builtins.int
    API_SHORT_NAME_FIELD_NUMBER: builtins.int
    GITHUB_LABEL_FIELD_NUMBER: builtins.int
    CODEOWNER_GITHUB_TEAMS_FIELD_NUMBER: builtins.int
    DOC_TAG_PREFIX_FIELD_NUMBER: builtins.int
    ORGANIZATION_FIELD_NUMBER: builtins.int
    LIBRARY_SETTINGS_FIELD_NUMBER: builtins.int
    PROTO_REFERENCE_DOCUMENTATION_URI_FIELD_NUMBER: builtins.int
    REST_REFERENCE_DOCUMENTATION_URI_FIELD_NUMBER: builtins.int
    @property
    def method_settings(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___MethodSettings]:
        """A list of API method settings, e.g. the behavior for methods that use the
        long-running operation pattern.
        """
        pass
    new_issue_uri: typing.Text = ...
    """Link to a *public* URI where users can report issues.  Example:
    https://issuetracker.google.com/issues/new?component=190865&template=1161103
    """

    documentation_uri: typing.Text = ...
    """Link to product home page.  Example:
    https://cloud.google.com/asset-inventory/docs/overview
    """

    api_short_name: typing.Text = ...
    """Used as a tracking tag when collecting data about the APIs developer
    relations artifacts like docs, packages delivered to package managers,
    etc.  Example: "speech".
    """

    github_label: typing.Text = ...
    """GitHub label to apply to issues and pull requests opened for this API."""

    @property
    def codeowner_github_teams(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """GitHub teams to be added to CODEOWNERS in the directory in GitHub
        containing source code for the client libraries for this API.
        """
        pass
    doc_tag_prefix: typing.Text = ...
    """A prefix used in sample code when demarking regions to be included in
    documentation.
    """

    organization: global___ClientLibraryOrganization.ValueType = ...
    """For whom the client library is being published."""

    @property
    def library_settings(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___ClientLibrarySettings]:
        """Client library settings.  If the same version string appears multiple
        times in this list, then the last one wins.  Settings from earlier
        settings with the same version string are discarded.
        """
        pass
    proto_reference_documentation_uri: typing.Text = ...
    """Optional link to proto reference documentation.  Example:
    https://cloud.google.com/pubsub/lite/docs/reference/rpc
    """

    rest_reference_documentation_uri: typing.Text = ...
    """Optional link to REST reference documentation.  Example:
    https://cloud.google.com/pubsub/lite/docs/reference/rest
    """

    def __init__(self,
        *,
        method_settings : typing.Optional[typing.Iterable[global___MethodSettings]] = ...,
        new_issue_uri : typing.Text = ...,
        documentation_uri : typing.Text = ...,
        api_short_name : typing.Text = ...,
        github_label : typing.Text = ...,
        codeowner_github_teams : typing.Optional[typing.Iterable[typing.Text]] = ...,
        doc_tag_prefix : typing.Text = ...,
        organization : global___ClientLibraryOrganization.ValueType = ...,
        library_settings : typing.Optional[typing.Iterable[global___ClientLibrarySettings]] = ...,
        proto_reference_documentation_uri : typing.Text = ...,
        rest_reference_documentation_uri : typing.Text = ...,
        ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["api_short_name",b"api_short_name","codeowner_github_teams",b"codeowner_github_teams","doc_tag_prefix",b"doc_tag_prefix","documentation_uri",b"documentation_uri","github_label",b"github_label","library_settings",b"library_settings","method_settings",b"method_settings","new_issue_uri",b"new_issue_uri","organization",b"organization","proto_reference_documentation_uri",b"proto_reference_documentation_uri","rest_reference_documentation_uri",b"rest_reference_documentation_uri"]) -> None: ...
global___Publishing = Publishing

class JavaSettings(google.protobuf.message.Message):
    """Settings for Java client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class ServiceClassNamesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    LIBRARY_PACKAGE_FIELD_NUMBER: builtins.int
    SERVICE_CLASS_NAMES_FIELD_NUMBER: builtins.int
    COMMON_FIELD_NUMBER: builtins.int
    library_package: typing.Text = ...
    """The package name to use in Java. Clobbers the java_package option
    set in the protobuf. This should be used **only** by APIs
    who have already set the language_settings.java.package_name" field
    in gapic.yaml. API teams should use the protobuf java_package option
    where possible.

    Example of a YAML configuration::

     publishing:
       java_settings:
         library_package: com.google.cloud.pubsub.v1
    """

    @property
    def service_class_names(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Configure the Java class name to use instead of the service's for its
        corresponding generated GAPIC client. Keys are fully-qualified
        service names as they appear in the protobuf (including the full
        the language_settings.java.interface_names" field in gapic.yaml. API
        teams should otherwise use the service name as it appears in the
        protobuf.

        Example of a YAML configuration::

         publishing:
           java_settings:
             service_class_names:
               - google.pubsub.v1.Publisher: TopicAdmin
               - google.pubsub.v1.Subscriber: SubscriptionAdmin
        """
        pass
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        library_package : typing.Text = ...,
        service_class_names : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common","library_package",b"library_package","service_class_names",b"service_class_names"]) -> None: ...
global___JavaSettings = JavaSettings

class CppSettings(google.protobuf.message.Message):
    """Settings for C++ client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___CppSettings = CppSettings

class PhpSettings(google.protobuf.message.Message):
    """Settings for Php client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___PhpSettings = PhpSettings

class PythonSettings(google.protobuf.message.Message):
    """Settings for Python client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___PythonSettings = PythonSettings

class NodeSettings(google.protobuf.message.Message):
    """Settings for Node client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___NodeSettings = NodeSettings

class DotnetSettings(google.protobuf.message.Message):
    """Settings for Dotnet client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class RenamedServicesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    class RenamedResourcesEntry(google.protobuf.message.Message):
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        KEY_FIELD_NUMBER: builtins.int
        VALUE_FIELD_NUMBER: builtins.int
        key: typing.Text = ...
        value: typing.Text = ...
        def __init__(self,
            *,
            key : typing.Text = ...,
            value : typing.Text = ...,
            ) -> None: ...
        def ClearField(self, field_name: typing_extensions.Literal["key",b"key","value",b"value"]) -> None: ...

    COMMON_FIELD_NUMBER: builtins.int
    RENAMED_SERVICES_FIELD_NUMBER: builtins.int
    RENAMED_RESOURCES_FIELD_NUMBER: builtins.int
    IGNORED_RESOURCES_FIELD_NUMBER: builtins.int
    FORCED_NAMESPACE_ALIASES_FIELD_NUMBER: builtins.int
    HANDWRITTEN_SIGNATURES_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    @property
    def renamed_services(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Map from original service names to renamed versions.
        This is used when the default generated types
        would cause a naming conflict. (Neither name is
        fully-qualified.)
        Example: Subscriber to SubscriberServiceApi.
        """
        pass
    @property
    def renamed_resources(self) -> google.protobuf.internal.containers.ScalarMap[typing.Text, typing.Text]:
        """Map from full resource types to the effective short name
        for the resource. This is used when otherwise resource
        named from different services would cause naming collisions.
        Example entry:
        "datalabeling.googleapis.com/Dataset": "DataLabelingDataset"
        """
        pass
    @property
    def ignored_resources(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """List of full resource types to ignore during generation.
        This is typically used for API-specific Location resources,
        which should be handled by the generator as if they were actually
        the common Location resources.
        Example entry: "documentai.googleapis.com/Location"
        """
        pass
    @property
    def forced_namespace_aliases(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Namespaces which must be aliased in snippets due to
        a known (but non-generator-predictable) naming collision
        """
        pass
    @property
    def handwritten_signatures(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """Method signatures (in the form "service.method(signature)")
        which are provided separately, so shouldn't be generated.
        Snippets *calling* these methods are still generated, however.
        """
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        renamed_services : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        renamed_resources : typing.Optional[typing.Mapping[typing.Text, typing.Text]] = ...,
        ignored_resources : typing.Optional[typing.Iterable[typing.Text]] = ...,
        forced_namespace_aliases : typing.Optional[typing.Iterable[typing.Text]] = ...,
        handwritten_signatures : typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common","forced_namespace_aliases",b"forced_namespace_aliases","handwritten_signatures",b"handwritten_signatures","ignored_resources",b"ignored_resources","renamed_resources",b"renamed_resources","renamed_services",b"renamed_services"]) -> None: ...
global___DotnetSettings = DotnetSettings

class RubySettings(google.protobuf.message.Message):
    """Settings for Ruby client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___RubySettings = RubySettings

class GoSettings(google.protobuf.message.Message):
    """Settings for Go client libraries."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    COMMON_FIELD_NUMBER: builtins.int
    @property
    def common(self) -> global___CommonLanguageSettings:
        """Some settings."""
        pass
    def __init__(self,
        *,
        common : typing.Optional[global___CommonLanguageSettings] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["common",b"common"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["common",b"common"]) -> None: ...
global___GoSettings = GoSettings

class MethodSettings(google.protobuf.message.Message):
    """Describes the generator configuration for a method."""
    DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
    class LongRunning(google.protobuf.message.Message):
        """Describes settings to use when generating API methods that use the
        long-running operation pattern.
        All default values below are from those used in the client library
        generators (e.g.
        [Java](https://github.com/googleapis/gapic-generator-java/blob/04c2faa191a9b5a10b92392fe8482279c4404803/src/main/java/com/google/api/generator/gapic/composer/common/RetrySettingsComposer.java)).
        """
        DESCRIPTOR: google.protobuf.descriptor.Descriptor = ...
        INITIAL_POLL_DELAY_FIELD_NUMBER: builtins.int
        POLL_DELAY_MULTIPLIER_FIELD_NUMBER: builtins.int
        MAX_POLL_DELAY_FIELD_NUMBER: builtins.int
        TOTAL_POLL_TIMEOUT_FIELD_NUMBER: builtins.int
        @property
        def initial_poll_delay(self) -> google.protobuf.duration_pb2.Duration:
            """Initial delay after which the first poll request will be made.
            Default value: 5 seconds.
            """
            pass
        poll_delay_multiplier: builtins.float = ...
        """Multiplier to gradually increase delay between subsequent polls until it
        reaches max_poll_delay.
        Default value: 1.5.
        """

        @property
        def max_poll_delay(self) -> google.protobuf.duration_pb2.Duration:
            """Maximum time between two subsequent poll requests.
            Default value: 45 seconds.
            """
            pass
        @property
        def total_poll_timeout(self) -> google.protobuf.duration_pb2.Duration:
            """Total polling timeout.
            Default value: 5 minutes.
            """
            pass
        def __init__(self,
            *,
            initial_poll_delay : typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            poll_delay_multiplier : builtins.float = ...,
            max_poll_delay : typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            total_poll_timeout : typing.Optional[google.protobuf.duration_pb2.Duration] = ...,
            ) -> None: ...
        def HasField(self, field_name: typing_extensions.Literal["initial_poll_delay",b"initial_poll_delay","max_poll_delay",b"max_poll_delay","total_poll_timeout",b"total_poll_timeout"]) -> builtins.bool: ...
        def ClearField(self, field_name: typing_extensions.Literal["initial_poll_delay",b"initial_poll_delay","max_poll_delay",b"max_poll_delay","poll_delay_multiplier",b"poll_delay_multiplier","total_poll_timeout",b"total_poll_timeout"]) -> None: ...

    SELECTOR_FIELD_NUMBER: builtins.int
    LONG_RUNNING_FIELD_NUMBER: builtins.int
    AUTO_POPULATED_FIELDS_FIELD_NUMBER: builtins.int
    selector: typing.Text = ...
    """The fully qualified name of the method, for which the options below apply.
    This is used to find the method to apply the options.
    """

    @property
    def long_running(self) -> global___MethodSettings.LongRunning:
        """Describes settings to use for long-running operations when generating
        API methods for RPCs. Complements RPCs that use the annotations in
        google/longrunning/operations.proto.

        Example of a YAML configuration::

         publishing:
           method_settings:
             - selector: google.cloud.speech.v2.Speech.BatchRecognize
               long_running:
                 initial_poll_delay:
                   seconds: 60 # 1 minute
                 poll_delay_multiplier: 1.5
                 max_poll_delay:
                   seconds: 360 # 6 minutes
                 total_poll_timeout:
                    seconds: 54000 # 90 minutes
        """
        pass
    @property
    def auto_populated_fields(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]:
        """List of top-level fields of the request message, that should be
        automatically populated by the client libraries based on their
        (google.api.field_info).format. Currently supported format: UUID4.

        Example of a YAML configuration:

         publishing:
           method_settings:
             - selector: google.example.v1.ExampleService.CreateExample
               auto_populated_fields:
               - request_id
        """
        pass
    def __init__(self,
        *,
        selector : typing.Text = ...,
        long_running : typing.Optional[global___MethodSettings.LongRunning] = ...,
        auto_populated_fields : typing.Optional[typing.Iterable[typing.Text]] = ...,
        ) -> None: ...
    def HasField(self, field_name: typing_extensions.Literal["long_running",b"long_running"]) -> builtins.bool: ...
    def ClearField(self, field_name: typing_extensions.Literal["auto_populated_fields",b"auto_populated_fields","long_running",b"long_running","selector",b"selector"]) -> None: ...
global___MethodSettings = MethodSettings

method_signature: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[google.protobuf.descriptor_pb2.MethodOptions, google.protobuf.internal.containers.RepeatedScalarFieldContainer[typing.Text]] = ...
"""A definition of a client library method signature.

In client libraries, each proto RPC corresponds to one or more methods
which the end user is able to call, and calls the underlying RPC.
Normally, this method receives a single argument (a struct or instance
corresponding to the RPC request object). Defining this field will
add one or more overloads providing flattened or simpler method signatures
in some languages.

The fields on the method signature are provided as a comma-separated
string.

For example, the proto RPC and annotation:

  rpc CreateSubscription(CreateSubscriptionRequest)
      returns (Subscription) {
    option (google.api.method_signature) = "name,topic";
  }

Would add the following Java overload (in addition to the method accepting
the request object):

  public final Subscription createSubscription(String name, String topic)

The following backwards-compatibility guidelines apply:

  * Adding this annotation to an unannotated method is backwards
    compatible.
  * Adding this annotation to a method which already has existing
    method signature annotations is backwards compatible if and only if
    the new method signature annotation is last in the sequence.
  * Modifying or removing an existing method signature annotation is
    a breaking change.
  * Re-ordering existing method signature annotations is a breaking
    change.
"""

default_host: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[google.protobuf.descriptor_pb2.ServiceOptions, typing.Text] = ...
"""The hostname for this service.
This should be specified with no prefix or protocol.

Example:

  service Foo {
    option (google.api.default_host) = "foo.googleapi.com";
    ...
  }
"""

oauth_scopes: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[google.protobuf.descriptor_pb2.ServiceOptions, typing.Text] = ...
"""OAuth scopes needed for the client.

Example:

  service Foo {
    option (google.api.oauth_scopes) = \\
      "https://www.googleapis.com/auth/cloud-platform";
    ...
  }

If there is more than one scope, use a comma-separated string:

Example:

  service Foo {
    option (google.api.oauth_scopes) = \\
      "https://www.googleapis.com/auth/cloud-platform,"
      "https://www.googleapis.com/auth/monitoring";
    ...
  }
"""

api_version: google.protobuf.internal.extension_dict._ExtensionFieldDescriptor[google.protobuf.descriptor_pb2.ServiceOptions, typing.Text] = ...
"""The API version of this service, which should be sent by version-aware
clients to the service. This allows services to abide by the schema and
behavior of the service at the time this API version was deployed.
The format of the API version must be treated as opaque by clients.
Services may use a format with an apparent structure, but clients must
not rely on this to determine components within an API version, or attempt
to construct other valid API versions. Note that this is for upcoming
functionality and may not be implemented for all services.

Example:

  service Foo {
    option (google.api.api_version) = "v1_20230821_preview";
  }
"""
