from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Form

from users.dependencies.users.user import UserHandling

from sqlalchemy.orm  import Session

from posts.utils import create_dir as post_create_dir

from general import get_session

import aiofiles

from posts.models import Category, NewsPost, Image, NewsPostComments

from posts.schemas import (NewsPostCreateSchema,
 UserSchema,

  CategoryResponseSchema,

   NewsPostResponseSchemain, CommentCreateSchema)

from sqlalchemy.exc import IntegrityError

from typing import List

router = APIRouter(prefix="/posts", tags=['posts'])

@router.get('/get')
async def get_post(session: Session = Depends(get_session)):
    post = session.query(NewsPost).all()
    return post

@router.post('/create-category')
async def category_create(code: str = Form(...), category_name: str = Form(...), session:Session = Depends(get_session)):
    if code != "a29oYToxMzFyNjNzaDI0bw==":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='code xato yoki bu yerga faqat heshlangan kod kerak')
    try:
        category = Category(name=category_name)
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    except IntegrityError:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category bor')

@router.get('categories/', response_model=List[CategoryResponseSchema])
async def get_categries(session:Session = Depends(get_session)):
    categories = session.query(Category).all()
    return categories        

@router.get('/get-post/{post_id}', response_model=list[NewsPostResponseSchemain])
async def get_post(post_id: int, session:Session = Depends(get_session) ):
    post = session.query(NewsPost).filter(NewsPost.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Post id yo'q")
    return [post]

@router.post("/create-post",  response_model=list[NewsPostResponseSchemain])
async def create_post(
    user: UserSchema = Depends(UserHandling().employee),
    files: list[UploadFile] = File(...),
    title: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    session: Session = Depends(get_session)):

    category = session.query(Category).filter(Category.id == category_id).first()

    if category is None:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category id mavjud emas ')
   
    post = NewsPost(user_id=user.id, title=title, description=description, category_id=category_id)

    session.add(post)

    session.flush()
    for file in files:

        file_dir_for_django = ""

        if file is not None:

            file_data = await post_create_dir(post_id=post.id, filename=file.filename)

            content = await file.read()  

            async with aiofiles.open(file_data['file_full_path'], 'wb') as out_file:

                file_dir_for_django = file_data['file_dir'] + file.filename

                await out_file.write(content)
            
            image = Image(image=file_dir_for_django, news_post_id=post.id)

            session.add(image)

    session.commit()
    session.refresh(post)
    return [post]

@router.put("/update-post/{post_id}",  response_model=list[NewsPostResponseSchemain])
async def create_post(
    post_id: int,
    user: UserSchema = Depends(UserHandling().employee),
    files: list[UploadFile] = File(...),
    title: str = Form(...),
    description: str = Form(...),
    category_id: int = Form(...),
    session: Session = Depends(get_session)):

    category = session.query(Category).filter(Category.id == category_id).first()

    if category is None:

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='category id mavjud emas ')
    
    post  = session.query(NewsPost).filter(NewsPost.id == post_id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='post id xato')
    
    
    post.title = title
    post.description = description
    post.category_id = category_id

    old_images = session.query(Image).filter(Image.news_post_id == post.id).all()
    for image in old_images:
        session.delete(image)

    for file in files:

        file_dir_for_django = ""

        if file is not None:

            file_data = await post_create_dir(post_id=post.id, filename=file.filename)

            content = await file.read()  

            async with aiofiles.open(file_data['file_full_path'], 'wb') as out_file:

                file_dir_for_django = file_data['file_dir'] + file.filename

                await out_file.write(content)
            
            image = Image(image=file_dir_for_django, news_post_id=post.id)

            session.add(image)

    session.commit()
    return [post]

@router.delete('/post-delete/{post_id}')
async def delete_post(post_id: int, user: UserSchema = Depends(UserHandling().employee), session: Session = Depends(get_session)):
    post = session.query(NewsPost).filter(NewsPost.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Post id xato')
    session.delete(post)
    session.commit()
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="o'chrildi")

@router.post("/create-comment-post/{post_id}")
async def create_comment(
    post_id:int,
    comment:CommentCreateSchema,
    session:Session = Depends(get_session), 
    user: UserSchema = Depends(UserHandling().user)):
    newspost = session.query(NewsPost).filter(NewsPost.id == post_id).first()
    if newspost is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Post id xato')
    comment_news = NewsPostComments(news_post_id=post_id, user_id=user.id, comment=comment.comment)
    session.add(comment_news)
    session.commit()
    return newspost


@router.put("/update-comment-post/{comment_id}")
async def update_comment(
    comment_id:int,
    comment:CommentCreateSchema,
    session:Session = Depends(get_session), 
    user: UserSchema = Depends(UserHandling().user)):
    comment_news = session.query(NewsPostComments).filter(NewsPostComments.id == comment_id).first()
    if comment_news is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Post id xato')

    if not comment_news.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='pst sizniki emas')
    comment_news.comment=comment.comment
    session.add(comment_news)
    session.commit()
    return newspost


@router.delete("delete-comment-post/{comment_id}")
async def delete_comment(
    comment_id:int,
    session:Session = Depends(get_session), 
    user: UserSchema = Depends(UserHandling().user)):
    comment_news = session.query(NewsPostComments).filter(NewsPostComments.id == comment_id).first()
    if not comment_news.user_id == user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='pst sizniki emas')
    session.delete(comment_news)
    session.commit()
    return comment_news