from . import console
from . import database

def list_tasks(
    priority=None,
    today=None,
    week=None,
    inprogress=None,
    completed=None
) -> list:
    '''
    List all the tasks based on the filters.
    '''
    order_by = "priority DESC"
    where_clause = []
    if week:
        where_clause.append("(deadline >= date('now', 'weekday 1', '-7 days') AND deadline < date('now', 'weekday 1', '+1 days'))")
    elif today:
        where_clause.append("(deadline = date('now'))")
    if inprogress or completed:
        clause = []
        if inprogress:
            clause.append("status = 'In Progress'")
        if completed:
            clause.append("status = 'Completed'")
        where_clause.append("(" + " OR ".join(clause) + ")")
    if priority:
        where_clause.append(f"priority = {priority}")
    if where_clause:
        where_clause = "WHERE " + " AND ".join(where_clause)
    else:
        where_clause = ""

    results = database.list_table(table='tasks', columns=['id', 'title',
        'parent_id', 'status', 'deadline', 'priority'],
        where_clause=where_clause,
        order_by=f"ORDER BY {order_by}")

    final_results = []
    for result in results:
        final_results.append({
            "id": result[0],
            "title": result[1],
            "parent_id": result[2],
            "status": result[3],
            "deadline": result[4] if result[4] else "None",
            "priority": result[5]
        })
    return final_results
