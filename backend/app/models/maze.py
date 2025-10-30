from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Maze(Base):
    
    __tablename__ = "mazes"
    
    id = Column(Integer, primary_key=True, index=True)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    grid = Column(Text, nullable=False)  
    start_x = Column(Integer, nullable=False)
    start_y = Column(Integer, nullable=False)
    end_x = Column(Integer, nullable=False)
    end_y = Column(Integer, nullable=False)
    algorithm = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    solutions = relationship("Solution", back_populates="maze", cascade="all, delete-orphan")


class Solution(Base):
    
    __tablename__ = "solutions"
    
    id = Column(Integer, primary_key=True, index=True)
    maze_id = Column(Integer, ForeignKey("mazes.id"), nullable=False)
    algorithm = Column(String(50), nullable=False)
    path = Column(Text, nullable=False)  
    steps = Column(Text, nullable=False)  
    nodes_explored = Column(Integer, nullable=False)
    path_length = Column(Integer, nullable=False)
    execution_time = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    maze = relationship("Maze", back_populates="solutions")