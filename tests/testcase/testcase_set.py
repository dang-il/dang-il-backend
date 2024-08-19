import os, sys, dotenv
dotenv.load_dotenv()
sys.path.append(os.getenv("BACKEND_PATH"))

from app.deps import get_user_coll, get_session_coll, get_session_cache, get_user_tasking_time_coll, get_user_space_coll
from app.schemas.database_dto.db_schemas import UserColl
import asyncio
from datetime import datetime, timezone

if(__name__ == "__main__"):

    user_coll = get_user_coll()
    session_coll = get_session_coll()
    session_cache = get_session_cache()
    user_space_coll = get_user_space_coll()
    tasking_time_coll = get_user_tasking_time_coll()

    documents = []
    friend_list = []
    # 친구 도큐먼트 8개
    for i in range(8):
        data = {
            "_id": str(i),
            "name": str(i),
            "email": str(i),
            "tag": str(i),
            
        }
        friend_list.append(str(i))
        documents.append(data)
    # 친구 아닌 도큐먼트 12개
    for i in range(8,20):
        data = {
            "_id": str(i),
            "name": str(i),
            "email": "test",
            "tag": "test"
        }
        
        documents.append(data)
    
        
    async def bundle_execute():
        session_test1 = {
            "_id": "test1",
            "identifier": "test1",
            "created_at": str(datetime.now(timezone.utc))
        }
        session_test2 = {
            "_id": "test2",
            "identifier": "test2",
            "created_at": str(datetime.now(timezone.utc))
        }
        
        # 묶어서 실행
        await asyncio.gather(session_cache.insert(session_test1), session_cache.insert(session_test2), session_coll.insert(session_test1), session_coll.insert(session_test2))

        # 테스트 데이터
        await user_coll.insert({
            "_id": "test1",
            "name": "‍test1",
            "email": "test1",
            "tag": "test1"
        })
        await user_coll.insert({
            "_id": "test2",
            "name": "‍test2",
            "email": "test2",
            "tag": "test2"
        })
        await user_space_coll.insert({
            "_id": "test1",
            "interior_data": [{
                "decor_id": "desk1",
                "location": (1.0, 2.0, 3.0)
            }]
        })
        await tasking_time_coll.insert({
            "_id": "test1",
            "today_tasking_time": {
                "total_time": 3600,
                "task_specific_time": {
                    "math": 1900,
                    "coding": 1700
                }
            },
            "previous_tasking_time": {
                "day1": {
                    "total_time": 10800,
                    "task_specific_time": {
                        "math": 5400,
                        "coding": 5400
                    },
                "day2": {
                    "total_time": 3600,
                    "task_specific_time": {
                        "math": 1000,
                        "coding": 2600
                    }
                }
            }
        }})
        # 친구 데이터에서 공간정보 예시 넣기
        await user_space_coll.insert({
            "_id": "0",
            "interior_data": [{
                "decor_id": "0",
                "location": (0.0, 0.0, 0.0)
            }]
        })
        await user_space_coll.insert({
            "_id": "1",
            "interior_data": [{
                "decor_id": "1",
                "location": (1.0, 1.0, 1.0)
            }]
        })
        await user_coll.insert(documents)
        await user_coll.update({"_id":"test1"}, {"$set": {"friend_list": friend_list}})

    asyncio.run(bundle_execute())


