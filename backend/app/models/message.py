from sqlalchemy import Column, String, DateTime, Text, ForeignKey, BigInteger, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger, ForeignKey("chat_history.id", ondelete="CASCADE"), nullable=False)
    speaker = Column(Text, nullable=False)  # 'user' ou 'agent'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relacionamentos
    chat = relationship("ChatHistory", back_populates="messages")
    
    # Índices
    __table_args__ = (
        Index('idx_messages_chat_id', 'chat_id'),
        Index('idx_messages_speaker', 'speaker'),
        Index('idx_messages_created_at', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Message(id={self.id}, chat_id={self.chat_id}, speaker='{self.speaker}')>" 