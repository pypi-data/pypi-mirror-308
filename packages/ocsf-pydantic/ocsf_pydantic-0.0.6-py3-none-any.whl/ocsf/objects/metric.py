from pydantic import BaseModel

class Metric(BaseModel):
    """
    The Metric object defines a simple name/value pair entity for a metric.
    """

    name: str # The name of the metric.
    value: str # The value of the metric.

