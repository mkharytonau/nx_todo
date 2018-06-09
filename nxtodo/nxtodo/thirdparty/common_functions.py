def create_filters(id=None, title=None, category=None, priority=None,
                   status=None, place=None, description=None, name=None):
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
    if description:
        filters['description'] = description
    if name:
        filters['name'] = name
    return filters

