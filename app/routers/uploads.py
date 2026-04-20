from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.property import Property
from app.models.property_image import PropertyImage
from app.models.user import User
from app.routers.properties import get_current_user
from app.core.config import settings
import cloudinary
import cloudinary.uploader

router = APIRouter()

# Configure Cloudinary
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET
)


@router.post("/{property_id}/images", status_code=201)
async def upload_image(
    property_id: int,
    file: UploadFile = File(...),
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

    # Check the user owns this property
    if property.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload images to your own listings"
        )

    # Check file is an image
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG and WebP images are allowed"
        )

    # Read file contents
    contents = await file.read()

    # Upload to Cloudinary
    upload_result = cloudinary.uploader.upload(
        contents,
        folder=f"real_estate/property_{property_id}",
        resource_type="image"
    )

    # Get the secure URL from Cloudinary
    image_url = upload_result["secure_url"]

    # Save the image URL to the database
    new_image = PropertyImage(
        property_id=property_id,
        image_url=image_url
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)

    return {"message": "Image uploaded successfully", "image_url": image_url}


@router.get("/{property_id}/images")
async def get_property_images(property_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PropertyImage).where(PropertyImage.property_id == property_id)
    )
    images = result.scalars().all()
    return images
