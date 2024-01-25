from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from src.auth.controllers import get_current_user
from src.auth.models import User
from src.post.models import Post
from src.post.schemas import PostBase, PostAddOut
from src.main import get_db
from typing import List, Annotated
from uuid import uuid4
import os
from cachetools import TTLCache

# Create a cache that expires after 5 minutes (300 seconds)
cache = TTLCache(maxsize=100, ttl=300)

router = APIRouter()

# Define a route for adding a post with a POST method. The response model will be PostAddOut.
@router.post("/posts")
def add_post(
    payload: Annotated[bytes|None, File()]=None,  # The payload of the post, which is a file or None.
    title: str = Form(),  # The title of the post, which is a form data.
    content: str = Form(),  # The content of the post, which is a form data.
    db: Session = Depends(get_db),  # The database session.
    current_user: User = Depends(get_current_user)  # The current user.
) -> PostAddOut:
    # Create a new Post object with the provided title and content.
    db_post = Post(title=title, content=content)
    # If a payload is provided,
    if payload:
        # If the size of the payload exceeds 1MB, raise an HTTPException with status 400 and a detail message "Payload size exceeds 1MB limit".
        if len(payload) > 1_000_000:
            raise HTTPException(status_code=400, detail='Payload size exceeds 1MB limit')
        # Get the path to the media directory.
        media_dir = os.path.join(os.getcwd(), 'media')
        # If the media directory does not exist, create it.
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
        # Generate a unique filename.
        filename = str(uuid4())
        # Get the path to the location where the file will be saved.
        file_location = os.path.join(media_dir, f"{db_post.id}_{filename}")
        # Open the file in write mode and write the payload to it.
        with open(file_location, "wb") as buffer:
            buffer.write(payload)
        # Set the payload of the post to the path of the saved file.
        db_post.payload = f"/media/{db_post.id}_{filename}"
    # Add the post to the database session.
    db.add(db_post)
    # Commit the changes to the database.
    db.commit()
    # Return the ID of the new post.
    return {"id": db_post.id}

# Define a route for getting all posts with a GET method. The response model will be a list of PostBase.
@router.get("/posts", response_model=List[PostBase])
def get_posts(
    db: Session = Depends(get_db),  # The database session.
    current_user: User = Depends(get_current_user)  # The current user.
):
    # If 'posts' is in the cache,
    if 'posts' in cache:
        # Return the cached posts.
        return cache['posts']
    # If 'posts' is not in the cache, query the database for all posts.
    posts = db.query(Post).all()
    # Add the posts to the cache.
    cache['posts'] = posts
    # Return the posts.
    return posts


# Define a route for deleting a post with a DELETE method. The response model will be PostBase.
@router.delete("/posts/{post_id}", response_model=PostBase)
def delete_post(
    post_id: int,  # The ID of the post to delete.
    db: Session = Depends(get_db),  # The database session.
    current_user: User = Depends(get_current_user)  # The current user.
):
    # Query the database for the post with the given ID.
    post = db.query(Post).filter(Post.id == post_id).first()
    # If no post is found, raise an HTTPException with status 404 and a detail message "Post not found".
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    # If a post is found, delete it from the database.
    db.delete(post)
    # Commit the changes to the database.
    db.commit()
    # Return the deleted post.
    return post