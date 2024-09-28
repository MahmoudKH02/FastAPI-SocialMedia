from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import Annotated

from .. import models, schemas
from ..database import get_db
from ..utils import oauth2

UPVOTE = 1
DOWNVOTE = 0

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(
    user_token: Annotated[schemas.TokenData, Depends(oauth2.get_current_user)],
    vote: schemas.VoteCreate,
    db: Session = Depends(get_db)
):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with ID {vote.post_id} does not exist!!')
    
    vote_query = db.query(models.Vote) \
        .filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_token.id)
    new_vote = vote_query.first()
    
    if vote.dir == UPVOTE:
        # Post already upvoted
        if new_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f'Post already voted for by the this user!!')
        db.add(models.Vote(post_id=vote.post_id, user_id=user_token.id))
        db.commit()

        return {"message": f"Vote succefully created for post {vote.post_id}"}

    elif vote.dir == DOWNVOTE:
        # Post already downvoted
        if new_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'No vote found for Post with id {vote.post_id} from current user!!')
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": f"Vote succefully removed for post {vote.post_id}"}
