from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import models, schemas
from ..database import get_db
from ..utils.security import get_current_admin, get_password_hash

router = APIRouter()

@router.post("/", response_model=schemas.UserInDB)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    # Verificar si el email ya existe
    existing_user = await db.execute(
        select(models.User).where(models.User.email == user.email)
    )
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    # Crear usuario
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[schemas.UserInDB])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    result = await db.execute(
        select(models.User)
        .offset(skip)
        .limit(limit)
        .order_by(models.User.created_at.desc())
    )
    return result.scalars().all()

@router.get("/{user_id}", response_model=schemas.UserInDB)
async def read_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.put("/{user_id}", response_model=schemas.UserInDB)
async def update_user(
    user_id: str,
    user_update: schemas.UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    db_user = await db.get(models.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # No permitir auto-edición de rol
    if db_user.id == current_user.id and user_update.role:
        raise HTTPException(status_code=400, detail="No puedes cambiar tu propio rol")
    
    update_data = user_update.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
async def delete_user(
    user_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    # No permitir auto-eliminación
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")
    
    user = await db.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Eliminación lógica
    user.is_active = False
    await db.commit()
    return {"message": "Usuario desactivado"}
