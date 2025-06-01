from fastapi import APIRouter, HTTPException, Header

from src.models.pydantic_schemas import ReviewIn, ReviewOut, AvgScore
from src.models.orm_models import Review
from src.repository.reviews_repo import reviews_repo

router = APIRouter()


@router.get('/product/avg_score/{product_id}', tags=['unauthorized'], response_model=AvgScore)
async def get_avg_score(product_id: int):
    score = await reviews_repo.get_avg_score_by_product_id(product_id)
    if score == None:
        raise HTTPException(404, 'There are no scores for this product')
    return {'score': float(score)}


@router.get('/product/{product_id}', tags=['unauthorized'], response_model=list[ReviewOut])
async def get_product_reviews(product_id: int):
    reviews = await reviews_repo.get_product_review_by_id(product_id)
    return reviews


@router.get('/user/{user_id}', tags=['unauthorized'], response_model=list[ReviewOut])
async def get_user_reviews(user_id: int):
    reviews = await reviews_repo.get_user_review_by_id(user_id)
    return reviews


@router.post(
    '/',
    tags=['authorized'],
    response_model=ReviewOut,
    status_code=201
)
async def insert_review(
    review: ReviewIn,
    x_user_id: str = Header(...),
    x_user_role: str = Header(...)
):
    if x_user_role != 'admin' and int(x_user_id) != review.user_id:
        raise HTTPException(403, 'You have no access')

    new_review = Review(
        user_id=review.user_id,
        product_id=review.product_id,
        review=review.review,
        score=review.score
    )

    new_review = await reviews_repo.insert_review(new_review)
    return new_review


@router.put(
    '/{id}',
    tags=['authorized'],
    response_model=ReviewOut,
    status_code=201
)
async def update_review(
    id: int,
    new_data: ReviewIn,
    x_user_id: str = Header(...),
    x_user_role: str = Header(...)
):
    if x_user_role != 'admin' and int(x_user_id) != new_data.user_id:
        raise HTTPException(403, 'You have no access')

    review = await reviews_repo.get_review_by_id(id)
    if review == None:
        raise HTTPException(404, 'The review does not exist')

    if x_user_role != 'admin' and int(x_user_id) != review.user_id:
        raise HTTPException(403, 'You have no access')

    review.user_id = new_data.user_id
    review.product_id = new_data.product_id
    review.review = new_data.review
    review.score = new_data.score

    review = await reviews_repo.update_review(review)
    return review


@router.delete('/{id}', tags=['authorized'], status_code=204)
async def delete_review(
    id: int,
    x_user_id: str = Header(...),
    x_user_role: str = Header(...)
):
    review = await reviews_repo.get_review_by_id(id)
    if x_user_role != 'admin' and int(x_user_id) != review.user_id:
        raise HTTPException(403, 'You have no access')
    if review == None:
        raise HTTPException(404, 'The provider does not exist')

    await reviews_repo.delete_review_by_id(id)
