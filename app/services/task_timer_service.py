from typing import Optional
from datetime import datetime, timedelta
from app.schemas.database_dto.db_schemas import UserTaskingTimeColl, TaskingTime
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.deps import get_user_tasking_time_coll

class TaskTimerService:
    instance: Optional["TaskTimerService"] = None

    @classmethod
    def get_instance(cls) -> "TaskTimerService":
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    async def start_task_timer(self, user_data, task_name: str, tasking_time_coll: MongoDBHandler = get_user_tasking_time_coll()):
        user_id = user_data["_id"]
        current_time = datetime.utcnow()

        tasking_data = await tasking_time_coll.select({"_id": user_id})
        
        if not tasking_data: 
            tasking_data = {
                "today_tasking_time": {"total_time": 0, "task_specific_time": {task_name: 0}},
                "previous_tasking_time": {},
            }

        if "start_time" in tasking_data:
            raise ValueError("Task already started.")

        tasking_data["start_time"] = current_time
        await tasking_time_coll.update({"_id": user_id}, tasking_data)

        return {
            "message": "Timer started.",
            "total_time": tasking_data["today_tasking_time"]["total_time"],
            "task_specific_time": tasking_data["today_tasking_time"]["task_specific_time"],
        }

    async def pause_task_timer(self, user_data, tasking_time_coll: MongoDBHandler = get_user_tasking_time_coll()):
        user_id = user_data["_id"]
        current_time = datetime.utcnow()

        tasking_data = await tasking_time_coll.select({"_id": user_id})
        if "start_time" not in tasking_data:
            raise ValueError("Task timer not started.")

        start_time = tasking_data["start_time"]
        elapsed_time = (current_time - start_time).total_seconds()

        tasking_data["today_tasking_time"]["total_time"] += elapsed_time
        tasking_data["today_tasking_time"]["task_specific_time"].setdefault(tasking_data["current_task"], 0)
        tasking_data["today_tasking_time"]["task_specific_time"][tasking_data["current_task"]] += elapsed_time

        del tasking_data["start_time"]
        await tasking_time_coll.update({"_id": user_id}, tasking_data)

        return {
            "message": "Timer paused.",
            "total_time": tasking_data["today_tasking_time"]["total_time"],
            "task_specific_time": tasking_data["today_tasking_time"]["task_specific_time"],
        }

    async def reset_task_timer(self, user_data, tasking_time_coll: MongoDBHandler = get_user_tasking_time_coll()):
        user_id = user_data["_id"]
        current_time = datetime.utcnow()

        tasking_data = await tasking_time_coll.select({"_id": user_id})

        if not tasking_data:
            raise ValueError("No tasking data found for this user.")

        today = current_time.strftime("%Y-%m-%d")
        tasking_data["previous_tasking_time"][today] = tasking_data["today_tasking_time"]

        tasking_data["today_tasking_time"] = {
            "total_time": 0,
            "task_specific_time": {}
        }

        await tasking_time_coll.update({"_id": user_id}, tasking_data)

        return {
            "message": "Timer reset and previous tasking time recorded.",
            "total_time": tasking_data["today_tasking_time"]["total_time"],
            "task_specific_time": tasking_data["today_tasking_time"]["task_specific_time"],
        }


def get_task_timer_service() -> TaskTimerService:
    return TaskTimerService.get_instance()
