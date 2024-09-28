from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Annotated, Optional

from .. import models, schemas
from ..database import get_db
from ..utils import oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])

# TODO: if the post is not published (False), then only the user that owns that post will be able ot see that post.
@router.get("/", response_model=List[schemas.PostVote])
def get_posts(
    db: Session = Depends(get_db),
    search: Optional[str] = "", limit: int = 10, skip: int = 0,
):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(skip).all()

    posts = list ( map (lambda x : x._mapping, posts) )

    return posts


# @router.get("/", response_model=List[schemas.Post])
# def get_posts(
#     user_token: Annotated[schemas.TokenData, Depends(oauth2.get_current_user)],
#     db: Session = Depends(get_db)
# ):
#     "This would only retrive the posts created by the currently logged int user"
#     posts = db.query(models.Post).filter(models.Post.owner_id == user_token.id).all()

#     return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    user_token: Annotated[schemas.TokenData, Depends(oauth2.get_current_user)],
    post: schemas.PostCreate, db: Session = Depends(get_db)
):
    new_post = models.Post(**post.model_dump(), owner_id=user_token.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.PostVote)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .filter(models.Post.id == id) \
        .join(models.Vote, isouter=True) \
        .group_by(models.Post.id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found!!')
    
    return post._mapping


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    user_token: Annotated[schemas.TokenData, Depends(oauth2.get_current_user)],
    id: int, db: Session = Depends(get_db)
):
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found!!')
    
    if post.owner_id != user_token.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'NOT Autharized to perform the requested action!!')
    
    query.delete(synchronize_session=False)
    db.commit()

    return {"message": "This should NOT return a message!!"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(
    user_token: Annotated[schemas.TokenData, Depends(oauth2.get_current_user)],
    id: int, post: schemas.PostUpdate,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post).filter(models.Post.id == id)
    old_post = query.first()

    if old_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id {id} was not found!!')
    
    if old_post.owner_id != user_token.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'NOT Autharized to perform the requested action!!')
    
    query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    return query.first()

