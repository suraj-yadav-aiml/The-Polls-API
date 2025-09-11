from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from app.models.Votes import VoteById, VoteByLabel, Vote, Voter
from app.models.Polls import Poll
from app.services import utils

router = APIRouter()

def common_validations(poll_id: UUID, vote: VoteById | VoteByLabel):
    poll = utils.get_poll(poll_id=poll_id)
    if not poll:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The poll was not found"
        )

    if not poll.is_active():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The poll has expired."
        )
    
    voter_email = vote.voter.email
    if utils.get_vote(poll_id=poll_id, email=voter_email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vote by email {voter_email} is already voted"
        )
    
    return poll
    

@router.post("/{poll_id}/id")
def vote_by_id(poll_id: UUID, vote: VoteById, poll: Poll = Depends(common_validations)):

    if vote.choice_id not in [choice.id for choice in poll.options]:
        raise HTTPException( 
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid choice id specified."
        )

    vote =  Vote(
        poll_id=poll_id,
        choice_id=vote.choice_id,
        voter=Voter(**vote.voter.model_dump())
    )
    utils.save_vote(
        poll_id=poll_id,
        vote=vote
    ) 
    return {
        'message': 'Vote Recorded !!!',
        'vote': vote
    }

@router.post("/{poll_id}/label")
def vote_by_label(poll_id: UUID, vote: VoteByLabel, poll: Poll = Depends(common_validations)):

    choice_id = utils.get_choice_id_by_label_given_poll(
        poll=poll,
        label=vote.choice_label
    )

    if not choice_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid choice label provided."
        )
    vote = Vote(
        poll_id=poll_id,
        choice_id=choice_id,
        voter=Voter(**vote.voter.model_dump())
    )
    utils.save_vote(
        poll_id=poll_id,
        vote=vote 
    )
    return {
        'message': 'Vote Recorded !!!',
        'vote': vote
    } 


