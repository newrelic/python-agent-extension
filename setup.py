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

from setuptools import setup

# Best practice: package name should be prefixed with `newrelic.extensions.`
INSTRUMENTED_PACKAGE = "sampleproject"
PACKAGE_NAME = "newrelic.extensions.{}".format(INSTRUMENTED_PACKAGE)
HOOKS = [
    # package_to_intercept = instrumentation_hook
    "sample = {}.example:instrument".format(PACKAGE_NAME)
]

setup(
    name=PACKAGE_NAME,
    version="0.1",
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: "src"},
    entry_points={"newrelic.hooks": HOOKS},
    license="Apache-2.0",
    classifiers=["License :: OSI Approved :: Apache Software License"],
    install_requires=[
        "newrelic",
        # Always require the package being instrumented
        INSTRUMENTED_PACKAGE,
    ],
)
