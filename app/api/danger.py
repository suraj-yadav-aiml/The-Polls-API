from fastapi import APIRouter, HTTPException, status
from uuid import UUID

from app.services import utils

router = APIRouter()


@router.delete("/{poll_id}")
def delete_poll(poll_id: UUID):
    poll_to_delete = utils.get_poll(poll_id=poll_id)
    poll_title = poll_to_delete.title
    if not poll_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="A poll by that ID does ot exist"
        )
    
    utils.delete_poll(poll_id=poll_id)

    return {
        "message": f"A poll with title {poll_title!r} is deleted successfully !!!"
    }