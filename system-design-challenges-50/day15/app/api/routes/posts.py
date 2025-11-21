from fastapi import APIRouter, Depends, HTTPException
from typing import List
from ..schemas.post_request import PostCreate
from ..schemas.post_response import PostResponse
from ...application.commands.create_post import CreatePostCommand
from ...application.queries.get_post import GetPostQuery
from ...application.queries.feed_query import FeedQuery
from ...application.handlers.command_handlers.create_post_handler import CreatePostHandler
from ...application.handlers.query_handlers.get_post_handler import GetPostHandler
from ...application.handlers.query_handlers.feed_query_handler import FeedQueryHandler

router = APIRouter()

@router.post("/posts", response_model=PostResponse)
async def create_post(post: PostCreate):
    command = CreatePostCommand(content=post.content, author=post.author)
    handler = CreatePostHandler()
    post_entity = handler.handle(command)
    return PostResponse(id=post_entity.id, content=post_entity.content, author=post_entity.author)

@router.get("/posts/{post_id}", response_model=PostResponse)
async def get_post(post_id: str):
    query = GetPostQuery(post_id=post_id)
    handler = GetPostHandler()
    post_entity = handler.handle(query)
    if not post_entity:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponse(id=post_entity.id, content=post_entity.content, author=post_entity.author)

@router.get("/feed", response_model=List[PostResponse])
async def get_feed(skip: int = 0, limit: int = 10):
    query = FeedQuery(skip=skip, limit=limit)
    handler = FeedQueryHandler()
    posts = handler.handle(query)
    return [PostResponse(id=post.id, content=post.content, author=post.author) for post in posts]