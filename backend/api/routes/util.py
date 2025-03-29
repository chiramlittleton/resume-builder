def clean_mongo_doc(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])  # Or use `del doc["_id"]` to remove it entirely
    return doc
