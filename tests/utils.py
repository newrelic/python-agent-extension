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

from newrelic.common.object_wrapper import transient_function_wrapper, function_wrapper


def validate_transaction_metrics(
    name, group="Function", web_transaction=False, metrics=()
):
    """Validate that certain metrics are created

    :param name: Name of the transaction
    :type name: str
    :param group: (optional) The group under which the transaction will appear
        in the UI. Default: 'Function'
    :type group: str
    :param web_transaction: (optional) Indicates if the transaction is a "web" transaction. Default: False
    :type web_transaction: bool
    :param metrics: (optional) A list of tuples in the form of (name, count)
        for metrics that are expected to be reported. Default: ()
    :type metrics: list or tuple

    The following example validates the a background task is created.

    Usage::

        >>> import newrelic.agent
        >>> @validate_transaction_metrics("example")
        ... def test_example():
        ...
        ...     @newrelic.agent.background_task(name="example")
        ...     def example():
        ...         pass
        ...
        ...     example()
        >>> test_example()
    """

    if web_transaction:
        expected_metrics = [
            ("HttpDispatcher", 1),
            ("WebTransaction", 1),
            ("WebTransaction/%s/%s" % (group, name), 1),
            ("WebTransactionTotalTime", 1),
            ("WebTransactionTotalTime/%s/%s" % (group, name), 1),
        ]
    else:
        expected_metrics = [
            ("OtherTransaction/all", 1),
            ("OtherTransaction/%s/%s" % (group, name), 1),
            ("OtherTransactionTotalTime", 1),
            ("OtherTransactionTotalTime/%s/%s" % (group, name), 1),
        ]

    expected_metrics.extend(metrics)

    @function_wrapper
    def _validate_wrapper(wrapped, instance, args, kwargs):

        record_transaction_called = []
        recorded_metrics = []

        @transient_function_wrapper(
            "newrelic.core.stats_engine", "StatsEngine.record_transaction"
        )
        def _validate_transaction_metrics(wrapped, instance, args, kwargs):
            record_transaction_called.append(True)
            try:
                result = wrapped(*args, **kwargs)
            except:
                raise
            else:
                metrics = instance.stats_table
                recorded_metrics.append(metrics)

            return result

        def _validate(metrics, name, count):
            key = (name, "")
            metric = metrics.get(key)

            def _metrics_table():
                out = [""]
                out.append("Expected: {0}: {1}".format(key, count))
                for metric_key, metric_value in metrics.items():
                    out.append("{0}: {1}".format(metric_key, metric_value[0]))
                return "\n".join(out)

            def _metric_details():
                return "metric=%r, count=%r" % (key, metric.call_count)

            if count is not None:
                assert metric is not None, _metrics_table()
                if count == "present":
                    assert metric.call_count > 0, _metric_details()
                else:
                    assert metric.call_count == count, _metric_details()

            else:
                assert metric is None, _metrics_table()

        _new_wrapper = _validate_transaction_metrics(wrapped)
        val = _new_wrapper(*args, **kwargs)
        assert record_transaction_called
        record_transaction_called.pop()
        recorded_metrics = recorded_metrics.pop()

        for name, count in expected_metrics:
            _validate(recorded_metrics, name, count)
        return val

    return _validate_wrapper
