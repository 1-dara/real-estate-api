from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class PropertyCreate(BaseModel):
    title: str
    description: str
    price: float
    location: str
    city: str
    state: str
    property_type: str
    bedrooms: int
    bathrooms: int
    size_sqm: Optional[float] = None
    amenities: Optional[List[str]] = []


class PropertyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    property_type: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    size_sqm: Optional[float] = None
    amenities: Optional[List[str]] = None
    is_available: Optional[bool] = None


class PropertyResponse(BaseModel):
    id: int
    owner_id: int
    title: str
    description: str
    price: float
    location: str
    city: str
    state: str
    property_type: str
    bedrooms: int
    bathrooms: int
    size_sqm: Optional[float] = None
    amenities: List[str]
    is_available: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
