from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.database import get_db
from app.models.review import Review
from app.models.property import Property
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewResponse
from app.routers.properties import get_current_user

router = APIRouter()

# Create a review


@router.post("/{property_id}/reviews", response_model=ReviewResponse, status_code=201)
async def create_review(
    property_id: int,
    review_data: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Check property exists
    result = await db.execute(select(Property).where(Property.id == property_id))
    property = result.scalar_one_or_none()

    if not property:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Property not found"
        )

    # Check user is not reviewing their own property
    if property.owner_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot review your own property"
        )

    # Check user hasn't already reviewed this property
    result = await db.execute(
        select(Review).where(
            Review.property_id == property_id,
            Review.author_id == current_user.id
        )
    )
    existing_review = result.scalar_one_or_none()
    if existing_review:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already reviewed this property"
        )

    # Create the review
    new_review = Review(
        property_id=property_id,
        author_id=current_user.id,
        rating=review_data.rating,
        comment=review_data.comment
    )

    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review


# Get all reviews for a property
@router.get("/{property_id}/reviews", response_model=List[ReviewResponse])
async def get_reviews(property_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Review).where(Review.property_id == property_id)
    )
    reviews = result.scalars().all()
    return reviews
