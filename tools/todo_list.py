class TodoTask:
    name_task = ""
    tags = []
    completed = False
    
    def __init__(self, name, tags, completed):
        self.name_task = name
        self.tags = tags
        self.completed = completed