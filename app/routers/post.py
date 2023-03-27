from typing import List

from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import schemas, models, oauth2
from app.database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Post"]
)


# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),
              current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10,
              skip: int = 0,
              search: str = ""):
    # cursor.execute("""
    # SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).all()

    # posts = db.query(models.Post) \
    #     .filter(models.Post.title.contains(search)) \
    #     .limit(limit=limit) \
    #     .offset(offset=skip) \
    #     .all()
    # return posts

    join_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id)

    # default is LEFT INNER JOIN -> have to use isouter=True to be LEFT OUTER JOIN
    # label() to customize column name from query

    # SELECT posts.id AS posts_id,
    # posts.title AS posts_title,
    # posts.content AS posts_content,
    # posts.published AS posts_published,
    # posts.created_at AS posts_created_at,
    # posts.owner_id AS posts_owner_id,
    # count(votes.post_id) AS votes
    # FROM posts LEFT OUTER JOIN votes
    # ON posts.id = votes.post_id
    # GROUP BY posts.id

    # results = join_query.all()
    # return results

    offset_limit_search_query = join_query\
        .filter(models.Post.title.contains(search))\
        .limit(limit=limit)\
        .offset(offset=skip)

    # SELECT posts.id AS posts_id,
    # posts.title AS posts_title,
    # posts.content AS posts_content,
    # posts.published AS posts_published,
    # posts.created_at AS posts_created_at,
    # posts.owner_id AS posts_owner_id,
    # count(votes.post_id) AS votes
    # FROM posts LEFT OUTER JOIN votes
    # ON posts.id = votes.post_id
    # WHERE (posts.title LIKE '%%' || %(title_1)s || '%%')
    # GROUP BY posts.id LIMIT %(param_1)s
    # OFFSET %(param_2)s

    results = offset_limit_search_query.all()
    return results


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db),
             user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    # SELECT * FROM posts
    # WHERE id = %s
    # """,
    #                (str(id)))
    # post = cursor.fetchone()

    # post = db.query(models.Post).filter(models.Post.id == id).first()

    join_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")) \
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
        .group_by(models.Post.id)
    post = join_query.filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    # INSERT INTO posts (title, content, published) VALUES
    # (%s, %s, %s)
    # RETURNING *
    # """,
    #                (post.title,
    #                 post.content,
    #                 post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=post.title, content=post.content, published=post.published)

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    # DELETE FROM posts
    # WHERE id = %s RETURNING *
    # """,
    #                (str(id)))
    # conn.commit()
    # deleted_post = cursor.fetchone()

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)

    deleted_post = deleted_post_query.first()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exits")

    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "post was successfully deleted"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,
                db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # cursor.execute("""
    # UPDATE posts SET title = %s, content = %s, published = %s
    # WHERE id = %s
    # RETURNING *
    # """,
    #                (post.title, post.content, post.published, str(id)))
    # conn.commit()
    # updated_post = cursor.fetchone()

    updated_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = updated_query.first()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exits")

    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")

    updated_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return updated_query.first()
