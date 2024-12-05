# Copyright 2017 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Helpers for providing client information.

Client information is used to send information about the calling client,
such as the library and Python version, to API services.
"""

from google.api_core import client_info


METRICS_METADATA_KEY = "x-goog-api-client"


class ClientInfo(client_info.ClientInfo):
    """Client information used to generate a user-agent for API calls.

    This user-agent information is sent along with API calls to allow the
    receiving service to do analytics on which versions of Python and Google
    libraries are being used.

    Args:
        python_version (str): The Python interpreter version, for example,
            ``'3.9.6'``.
        grpc_version (Optional[str]): The gRPC library version.
        api_core_version (str): The google-api-core library version.
        gapic_version (Optional[str]): The version of gapic-generated client
            library, if the library was generated by gapic.
        client_library_version (Optional[str]): The version of the client
            library, generally used if the client library was not generated
            by gapic or if additional functionality was built on top of
            a gapic client library.
        user_agent (Optional[str]): Prefix to the user agent header. This is
            used to supply information such as application name or partner tool.
            Recommended format: ``application-or-tool-ID/major.minor.version``.
        rest_version (Optional[str]): A string with labeled versions of the
            dependencies used for REST transport.
    """

    def to_grpc_metadata(self):
        """Returns the gRPC metadata for this client info."""
        return (METRICS_METADATA_KEY, self.to_user_agent())


DEFAULT_CLIENT_INFO = ClientInfo()
