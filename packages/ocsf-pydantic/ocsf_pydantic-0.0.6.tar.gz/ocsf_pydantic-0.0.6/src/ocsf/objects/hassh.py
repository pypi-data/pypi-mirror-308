from .fingerprint import Fingerprint

from pydantic import BaseModel

class HASSH(BaseModel):
    """
    The HASSH object contains SSH network fingerprinting values for specific
    client/server implementations. It provides a standardized way of identifying and
    categorizing SSH connections based on their unique characteristics and behavior.
    """

    fingerprint: Fingerprint  # The hash of the key exchange, encryption, authentication
                              # and compression algorithms.

    # Recommended:
    algorithm: str | None = None # The concatenation of key exchange, encryption, authentication and
                                 # compression algorithms (separated by ';'). NOTE: This is not the
                                 # underlying algorithm for the hash implementation.
