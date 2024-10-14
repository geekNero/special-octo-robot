class Tree:

    def __init__(self, task={}, table_name=None):
        if table_name is not None:
            self.val = table_name
        else:
            self.val = f"Title:{task['title']}\nPriority:{task['priority']} | Deadline:{task['deadline']}| Status:{task['status']}"
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return child

    def modify_title(self, task):
        self.val = f"Title:{task['title']}\nPriority:{task['priority']} | Deadline:{task['deadline']}| Status:{task['status']}"
