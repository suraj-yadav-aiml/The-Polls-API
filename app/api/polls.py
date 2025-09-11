from fastapi import APIRouter, status, HTTPException
from uuid import UUID
from enum import Enum

from app.models.Polls import PollCreate, Poll
from app.services import utils


router = APIRouter()

@router.post("/create")
def create_poll(poll: PollCreate) -> dict:
    new_poll:Poll = poll.create_poll()
    utils.save_poll(poll=new_poll)

    return {
        "details": "Poll successfully created",
        "poll_id": new_poll.id,
        "poll": new_poll
    } 

@router.get("/{poll_id}")
def get_poll(poll_id: UUID):
    poll = utils.get_poll(poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A poll with id {poll_id} was not found"
        )
    return poll 


class PollStatus(Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    ALL = 'all'


@router.get("/")
def get_polls(poll_status: PollStatus = PollStatus.ACTIVE):
    polls = utils.get_all_polls()
    if not polls:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No polls were found"
        )
    
    if poll_status == PollStatus.ACTIVE:
        filtered_polls = [
            poll for poll in polls
            if poll.is_active()
        ]
    elif poll_status == PollStatus.EXPIRED:
        filtered_polls = [
            poll for poll in polls
            if not poll.is_active()
        ]
    else:
        filtered_polls = polls

    return {
        "count": len(filtered_polls),
        "polls": filtered_polls
    }


@router.get("/{poll_id}/result")
def get_results(poll_id: UUID):

    return {
        'results': utils.get_poll_results(poll_id=poll_id)
    } 