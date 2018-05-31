def create_filters(id, title, category, priority, status, place=None):
    filters = {}
    if id:
        filters['id'] = id
    if title:
        filters['title'] = title
    if category:
        filters['category'] = category
    if priority:
        filters['priority'] = priority
    if status:
        filters['status'] = status
    if place:
        filters['place'] = place
    return filters

