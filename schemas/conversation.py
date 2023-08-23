conversation = {
    "type": "object",
    "properties": {
        "body": {
            "type": "object",
            "properties": {
                "s3_bucket": {"type": "string"},
                "s3_key": {"type": "string"},
                "title": {"type": "string"},
                "isPublic": {"type": "boolean"},
                "createdDate": {
                    "type": "string",
                    "format": "date"
                },
                "userID": {"type": "integer"},
                "topicID": {"type": "integer"}
            },
            "required": ["s3_bucket", "s3_key", "title", "isPublic", "createdDate", "userID", "topicID"]
        }
    },
    "required": ["body"]
}
