from sqlalchemy import Column, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from .base import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)  # 'inventory', 'movements', 'custom'
    format = Column(String, nullable=False)  # 'csv', 'excel', 'pdf'
    filters = Column(JSON)  # Parámetros de filtrado
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    file_path = Column(String)  # Ruta al archivo generado
