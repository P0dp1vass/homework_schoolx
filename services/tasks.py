from schemas.tasks import BaseTask, CreateTask, EditTask

tasks = []

class TaskService:
    def __init__(self):
        self.user_tasks = tasks
    
    def add_task(self, new_task: CreateTask):
        for task in self.user_tasks:
            if task.name == new_task.name:
                return {
                    "status": "task creation failed",
                    "reason": "task with this name already exists"
                }
            if task.description == new_task.description:
                return {
                    "status": "task creation failed",
                    "reason": "task with this description already exists"
                }
        self.user_tasks.append(new_task)
        return BaseTask(**new_task.model_dump())
    
    def get_all_tasks(self):
        print(tasks)
        return [BaseTask(**task.model_dump()) for task in self.user_tasks]

    def delete_task(self, task_name: str):
        for index, task in enumerate(self.user_tasks):
            if task.name == task_name:
                self.user_tasks.pop(index)
                return {
                    "status": "task deleted"
                }
        return {
            "status": "task deletion failed",
            "reason": "task not found"
        }

    def edit_task(self, task_name: str, edited_task: EditTask):
        task_to_edit_index = None
        for index, task in enumerate(self.user_tasks):
            if task.name == task_name:
                task_to_edit_index = index
                continue
            if task.name == edited_task.name:
                return {
                    "status": "task editing failed",
                    "reason": "task with this name already exists"
                }
            if task.description == edited_task.description:
                return {
                    "status": "task editing failed",
                    "reason": "task with this description already exists"
                }
        if task_to_edit_index is None:
            return {
                "status": "task editing failed",
                "reason": "task not found"
            }
        current_task = self.user_tasks[task_to_edit_index]
        updated_task = current_task.model_copy(update=edited_task.model_dump())
        self.user_tasks[task_to_edit_index] = updated_task
        return BaseTask(**updated_task.model_dump())