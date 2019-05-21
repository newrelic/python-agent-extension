# Copyright 2019 New Relic, Inc.
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

import newrelic.agent
import os
import pytest


@pytest.fixture(scope="session", autouse=True)
def agent():
    """Register the New Relic agent

    The agent must be initialized and enabled before any tests run.
    """
    settings = newrelic.agent.global_settings()

    # Set the app name to something descriptive
    settings.app_name = "extension_testing"

    # If the license key is not available, force developer mode on
    if not settings.license_key:
        settings.developer_mode = True

    # Set startup and shutdown timeouts
    settings.startup_timeout = float(os.environ.get("NEW_RELIC_STARTUP_TIMEOUT", 20.0))
    settings.shutdown_timeout = float(
        os.environ.get("NEW_RELIC_SHUTDOWN_TIMEOUT", 20.0)
    )

    # Initializing the agent sets up the import interceptor
    newrelic.agent.initialize()

    # Force application registration to fully enable the agent
    newrelic.agent.register_application()

    yield

    # Shutdown the agent when the tests terminate
    newrelic.agent.shutdown_agent()
