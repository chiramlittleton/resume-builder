# utils/mongo.py

from typing import Union, List

def clean_for_rest(data: Union[dict, List[dict]]):
    """Converts _id to string (used in REST)."""
    def _clean(doc: dict):
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    if isinstance(data, list):
        return [_clean(doc) for doc in data]
    return _clean(data)

def clean_for_gql(data: Union[dict, List[dict]]):
    """Removes _id field (used in GraphQL)."""
    def _clean(doc: dict):
        doc.pop("_id", None)
        return doc

    if isinstance(data, list):
        return [_clean(doc) for doc in data]
    return _clean(data)
