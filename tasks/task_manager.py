class TaskManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def create_task(self, title, description=""):
        task = {
            "id": self.next_id,
            "title": title,
            "description": description,
            "status": "waiting_approval",
            "approved": False,
        }

        self.tasks.append(task)
        self.next_id += 1
        return task

    def approve_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["approved"] = True
                task["status"] = "approved"
                return task

        return None

    def get_tasks(self):
        return self.tasks


if __name__ == "__main__":
    manager = TaskManager()

    task = manager.create_task(
        "Test Task",
        "Testing the Master Agent task system"
    )

    print("📋 Task Manager فعال شد.")
    print("🆔 Task ID:", task["id"])
    print("📌 وضعیت:", task["status"])
    print("🔐 تأیید مالک:", task["approved"])
