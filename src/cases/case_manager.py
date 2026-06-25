import uuid
import time
import redis
from utils.settings import REDIS_URL
from utils.logger import get_logger

logger = get_logger("case_manager")
r = redis.Redis.from_url(REDIS_URL)

CASE_HASH = "osprey:cases"
CASE_LIST = "osprey:case_list"


def create_case(alert_message: str, severity: str, analyst: str = "unassigned"):
    case_id = str(uuid.uuid4())
    ts = time.strftime("%Y-%m-%d %H:%M:%S")

    case = {
        "id": case_id,
        "message": alert_message,
        "severity": severity,
        "status": "open",
        "analyst": analyst,
        "created_at": ts,
        "updated_at": ts,
    }

    r.hset(CASE_HASH, case_id, str(case))
    r.lpush(CASE_LIST, case_id)

    logger.info(f"Case created: {case_id} ({severity})")
    return case_id


def update_case(case_id: str, status: str = None, analyst: str = None):
    raw = r.hget(CASE_HASH, case_id)
    if not raw:
        raise ValueError("Case not found")

    case = eval(raw.decode())  # simple, replace with json if preferable

    if status:
        case["status"] = status
    if analyst:
        case["analyst"] = analyst
    case["updated_at"] = time.strftime("%Y-%m-%d %H:%M:%S")

    r.hset(CASE_HASH, case_id, str(case))
    logger.info(f"Case updated: {case_id} -> {case}")
    return case


def list_cases(limit: int = 50):
    ids = r.lrange(CASE_LIST, 0, limit - 1)
    cases = []
    for cid in ids:
        raw = r.hget(CASE_HASH, cid.decode())
        if raw:
            cases.append(eval(raw.decode()))
    return cases
