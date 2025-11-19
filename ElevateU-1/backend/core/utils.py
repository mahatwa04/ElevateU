def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

def calculate_ranking(likes, comments, follows):
    return likes * 2 + comments * 1 + follows * 3

def format_achievement_data(data):
    return {
        "title": data.get("title", ""),
        "description": data.get("description", ""),
        "field": data.get("field", ""),
        "timestamp": data.get("timestamp", None),
    }