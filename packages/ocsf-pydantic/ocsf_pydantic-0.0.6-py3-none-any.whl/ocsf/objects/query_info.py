from ._entity import Entity

from datetime import datetime

class QueryInformation(Entity):
    """
    The query info object holds information related to data access within a
    datastore. To access, manipulate, delete, or retrieve data from a datastore, a
    query must be written using a specific syntax.
    """

    query_string: str # A string representing the query code being run. For example:
                      # `SELECT * FROM my_table`


    # Optional:
    query_time: datetime | None = None # The time when the query was run.
    data: dict | None = None # The data returned from the query execution.
    bytes: int | None = None # The size of the data returned from the query.
    name: str | None = None # The query name for a saved or scheduled query.
    uid: str | None = None # The unique identifier of the query.
