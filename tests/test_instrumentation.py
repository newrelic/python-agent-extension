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

import pytest
from utils import validate_transaction_metrics

# Always import the code under test within the test. This makes sure the agent
# is initialized prior to any import hooks being fired.
@pytest.fixture
def sample():
    import sample

    return sample


@validate_transaction_metrics("sample:main")
def test_instrumentation(sample):
    sample.main()
