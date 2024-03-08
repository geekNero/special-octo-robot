import console
import database

def list_tasks(
    priority: int,
    today: bool,
    week: bool,
    inprogress: bool,
    completed: bool
) -> list:
    '''
    List all the tasks based on the filters.
    '''
    order_by = "priority DESC"
    where_clause = []
    if today:
        where_clause.append("deadline = date('now')")
    elif week:
        where_clause.append("deadline BETWEEN date('now') AND date('now', '+7 days')")
    if inprogress:
        where_clause.append("status = 'In Progress'")
    elif completed:
        where_clause.append("status = 'Completed'")
    if priority:
        where_clause.append(f"priority = {priority}")
    results = list_table(table='tasks', columns=['title',
        'parent_id', 'status', 'deadline', 'priority'],
        where_clause="WHERE " + " AND ".join(where_clause),
        order_by=f"ORDER BY {order_by}")
    )
    return results
