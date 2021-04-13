import redis
import json
from aion.logger import lprint
from aion.microservice import main_decorator, Options, WITH_KANBAN

SERVICE_NAME = "get-response-of-face-api"
DEFAULT_REDIS_HOST = "redis-cluster"

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(host=DEFAULT_REDIS_HOST, port=6379)
    
    def hmset(self, key, value):
        self.client.hmset(key, value)

@main_decorator(SERVICE_NAME, WITH_KANBAN)
def main(opt: Options):
    conn = opt.get_conn()
    num = opt.get_number()
    for kanban in conn.get_kanban_itr(): 
        prior_res = kanban.get_result()
        redis_key = int(kanban.get_metadata().get("rediskey"))
        customer = kanban.get_metadata().get("status")
        lprint("redis keys is " + str(redis_key))
        lprint("customer status is " + str(customer))
        if prior_res and customer == "existing":
            data = {
                "status": "success",
                "customer": customer,
                "guest_id": int(kanban.get_metadata().get("guest_id")),
                "failed_ms": ""
            }
            lprint(data)
        elif prior_res and customer == "new":
            data = {
                "status": "success",
                "customer": customer,
                "age_by_face": int(kanban.get_metadata().get("age")),
                "gender_by_face": kanban.get_metadata().get("gender"),
                "image_path": kanban.get_metadata().get("filepath")
                # "face_rectangle": kanban.get_metadata().get("face_rectangle")
            }
        else:
            data = {
                "status": "failed",
                "customer": "",
                "guest_id": "",
                "failed_ms": kanban.get_metadata().get("microservice") 
            }
            lprint(data)
        try:
            rc = RedisClient()
            rc.hmset(redis_key, data)
        except Exception as e:
            lprint(str(e))

if __name__ == "__main__":
    main()
