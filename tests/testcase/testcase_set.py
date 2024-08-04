import os, sys, dotenv
dotenv.load_dotenv()
sys.path.append(os.getenv("BACKEND_PATH"))

from app.deps import get_user_coll, get_session_cache
from app.schemas.database_dto.db_schemas import UserColl
import asyncio
from datetime import datetime, timezone

if(__name__ == "__main__"):

    user_coll = get_user_coll()
    session_cache = get_session_cache()

    documents = []
    friend_list = []
    for i in range(8):
        data = {
            "_id": str(i),
            "name": str(i),
            "email": "test",
            "tag": "test"
        }
        
        friend_list.append(str(i))
        documents.append(data)

    for i in range(8,40):
        data = {
            "_id": str(i),
            "name": str(i),
            "email": "test",
            "tag": "test"
        }
        
        documents.append(data)
        
    async def bundle_execute():
        await session_cache.insert({
            "_id": "test1",
            "identifier": "test1",
            "created_at": str(datetime.now(timezone.utc))
        })
        await session_cache.insert({
            "_id": "test2",
            "identifier": "test2",
            "created_at": str(datetime.now(timezone.utc))
        })
        await user_coll.insert({
            "_id": "test1",
            "name": "‍테스트",
            "email": "test@khu.ac.kr",
            "tag": "1"
        })
        await user_coll.insert({
            "_id": "test2",
            "name": "‍테스트2",
            "email": "test2@khu.ac.kr",
            "tag": "2"
        })
        await user_coll.insert(documents)
        await user_coll.update({"_id":"107945448565645846942"}, {"$set": {"friend_list": friend_list}})

    asyncio.run(bundle_execute())


