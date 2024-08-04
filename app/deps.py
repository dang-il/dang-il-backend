# db 스키마
from app.utils.db_handlers.mongodb_handler import MongoDBHandler
from app.utils.db_handlers.redis_handler import RedisHandler
from app.utils.etc.server_sent_event import UserQueue
from app.utils.db_handlers.set_mongodb_ttl import set_mongodb_ttl
from app.schemas.database_dto.db_schemas import UserColl, SessionColl, UserSpaceColl, UserTaskingTimeColl, FriendWaitColl, DecorColl

# session_coll은 ttl설정
def get_session_coll() -> MongoDBHandler:
    db_settings = {
        "db_name": "artisticsw_db",
        "coll_name": "session_coll",
        "db_schema": SessionColl
    }
    mongodb_instance = MongoDBHandler(db_settings=db_settings)
    
    set_mongodb_ttl([("created_at", 1)], 86400*3, db_settings=db_settings)
    
    return mongodb_instance

def get_user_coll() -> MongoDBHandler:
    return MongoDBHandler(db_settings={
        "db_name": "artisticsw_db",
        "coll_name": "user_coll",
        "db_schema": UserColl
    })

def get_session_cache() -> RedisHandler:
    return RedisHandler(db_setting={
        "db_name": "0",
        "db_schema": SessionColl
    })

def get_user_space_coll() -> MongoDBHandler:
    return MongoDBHandler(db_settings={
        "db_name": "artisticsw_db",
        "coll_name": "user_space_coll",
        "db_schema": UserSpaceColl
    })
    
def get_user_tasking_time_coll() -> MongoDBHandler:
    return MongoDBHandler(db_settings={
        "db_name": "artisticsw_db",
        "coll_name": "user_space_coll",
        "db_schema": UserTaskingTimeColl
    })

def get_friend_wait_coll() -> MongoDBHandler:
    db_settings={
        "db_name": "artisticsw_db",
        "coll_name": "friend_wait_coll",
        "db_schema": FriendWaitColl
    }
    mongodb_instance = MongoDBHandler(db_settings=db_settings)
    set_mongodb_ttl([("request_date", 1)], 86400*3, db_settings=db_settings)
    
    return mongodb_instance

def get_decor_coll() -> MongoDBHandler:
    return MongoDBHandler(db_settings={
        "db_name": "artisticsw_db",
        "coll_name": "decor_coll",
        "db_schema": DecorColl
    })
    
def get_user_queue():
    user_q = UserQueue()
    return user_q.get_queue()

  

# def get_decor_coll() -> MongoDBHandler:
#     return MongoDBHandler(coll_config={"coll_name": "decor_coll"})

# def get_decor_category()->list:
#     return ['desk', 'lamp', 'monitor', 'vase', 'bookshelf', 'frame'] # 현재는 이정도
