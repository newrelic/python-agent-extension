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

"""Instrumentation module
"""
from newrelic.agent import wrap_background_task


def instrument(module):
    """Instrumentation hook entrypoint

    This function will be run on import
    of a module as specified in the setup.py

    :param module: The module that has been imported in the application.
    :type module: module
    """
    wrap_background_task(module, "main")
