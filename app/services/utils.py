import os
from typing import Dict, Optional, List
from dotenv import load_dotenv
from upstash_redis import Redis
from uuid import UUID

from app.models.Polls import Poll
from app.models.Votes import Vote
from app.models.Results import Result, PollResult

load_dotenv()


redis_client = Redis(
    url=os.getenv("REDIS_URL"),
    token=os.getenv("REDIS_TOKEN"),
)

def save_poll(poll: Poll) -> None:
    poll_json = poll.model_dump_json()
    redis_client.set(f"poll:{poll.id}", poll_json)

def get_poll(poll_id: UUID) -> Optional[Poll]:
    poll_json = redis_client.get(f"poll:{poll_id}")
    if poll_json:
        return Poll.model_validate_json(json_data=poll_json)
    return None

def get_all_polls() -> List[Poll]:
    
    poll_keys = redis_client.keys(pattern="poll:*")
    poll_jsons = redis_client.mget(*poll_keys)
    polls = [
        Poll.model_validate_json(json_data=pj)
        for pj in poll_jsons
        if pj
    ]
    return polls 


def get_choice_id_by_label(poll_id:UUID, label: int) -> Optional[UUID]:
    poll = get_poll(poll_id=poll_id)
    return get_choice_id_by_label_given_poll(poll=poll, label=label)

    # if poll:
    #     for choice in  poll.options:
    #         if choice.label == label:
    #             return choice.id
    # return None  

def get_choice_id_by_label_given_poll(poll: Poll, label: int) -> Optional[UUID]:
    if poll:
        for choice in  poll.options:
            if choice.label == label:
                return choice.id
    return None


def save_vote(poll_id:UUID, vote: Vote) -> None:
    vote_json = vote.model_dump_json()
    redis_client.hset(f"vote:{poll_id}", vote.voter.email, vote_json)
    redis_client.hincrby(key=f"vote_count:{poll_id}", field=str(vote.choice_id), increment=1)

def get_vote(poll_id: UUID, email: str) -> Optional[Vote]:
    vote_json = redis_client.hget(f"vote:{poll_id}", email)
    if vote_json:
        return Vote.model_validate_json(json_data=vote_json)
    return None 

def get_vote_counts(poll_id: UUID) -> Dict[UUID, int]:

    vote_counts = redis_client.hgetall(key=f"vote_count:{poll_id}")

    return {
        UUID(choice_id): int(count)
        for choice_id, count in vote_counts.items()
    }
    
def get_poll_results(poll_id: UUID):

    poll = get_poll(poll_id=poll_id)
    if not poll:
        return None
    
    vote_count = get_vote_counts(poll_id=poll_id)

    result = [
            Result(description=choice.description, vote_count=vote_count.get(choice.id, 0))
            for choice in poll.options
        ]
    
    result.sort(key=lambda x: x.vote_count, reverse=True)

    return PollResult(
        title=poll.title,
        total_votes=sum(vote_count.values()),
        result=result
    )

def delete_poll(poll_id: UUID) -> None:

    keys_to_delete = [
        f"poll:{poll_id}",
        f"vote:{poll_id}",
        f"vote_count:{poll_id}"
    ]

    redis_client.delete(*keys_to_delete)
