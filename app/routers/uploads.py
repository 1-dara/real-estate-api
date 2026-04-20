from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.property import Property
from app.models.property_image import PropertyImage
from app.models.user import User
from app.routers.properties import get_current_user
import os
import uuid

router = APIRouter()

# Where images will be saved on your computer
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


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

    # Generate a unique filename so images never overwrite each other
    extension = file.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    # Save the file to disk
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    # Save the image URL to the database
    image_url = f"/uploads/{unique_filename}"
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
