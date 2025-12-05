import uuid
from sqlalchemy import create_engine, Column, String, ForeignKey, DateTime, Text, Integer, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from db.base import Base


class SecretModel(Base):
    """
    This table stores agent information, including agent ID, API key, user ID, and other fields.
    """
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-increment ID
    assis_id = Column(String(255), unique=True, nullable=False)  # Store assistant object ID
    api_key = Column(String(768), unique=True, nullable=False)  # Restrict api_key to be unique
    user_id = Column(String(255), unique=True, nullable=False)  # Added user ID field

    initialized = Column(Boolean, default=False)  # Default value is false, determine if initialization has been performed
    agent_type = Column(String(255), default="normal")  # Default value is "normal"

    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Automatically generate creation time
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Message update time

    threads = relationship("ThreadModel", back_populates="agent", cascade="all, delete-orphan")


class ThreadModel(Base):
    """
    This table stores conversation thread information, each thread is associated with an agent and may contain multiple messages and knowledge bases.
    """
    __tablename__ = 'threads'
    id = Column(String(255), primary_key=True)
    agent_id = Column(String(255), ForeignKey('agents.assis_id'))
    conversation_name = Column(String(255))
    run_mode = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # Message update time

    # Reverse relationship to MessageModel
    messages = relationship("MessageModel", back_populates="thread", order_by="MessageModel.created_at")

    # Other relationship definitions
    knowledge_bases = relationship("KnowledgeBase", back_populates="thread")
    agent = relationship("SecretModel", back_populates="threads")


class KnowledgeBase(Base):
    """
    This table stores knowledge base information, including knowledge base name, chunking strategy, description, etc.
    """
    __tablename__ = 'knowledge_bases'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # Primary key field
    vector_store_id = Column(String(255), nullable=True)
    # Add strategy for text chunking
    chunking_strategy = Column(String(255), default="auto")
    max_chunk_size_tokens = Column(Integer, default=800)
    chunk_overlap_tokens = Column(Integer, default=400)

    # Knowledge base name
    knowledge_base_name = Column(String(255), nullable=False)

    # New field: record creation time
    created_at = Column(DateTime, default=func.now())
    # Display knowledge base name
    display_knowledge_base_name = Column(String(255), nullable=False)
    # Knowledge base description
    knowledge_base_description = Column(Text, nullable=True)
    # Foreign key field, linked to the id field in threads table
    thread_id = Column(String(255), ForeignKey('threads.id'))
    # Establish relationship with ThreadModel
    thread = relationship("ThreadModel", back_populates="knowledge_bases")
    files = relationship("FileInfo", back_populates="knowledge_base")  # File relationship


class FileInfo(Base):
    """
    This table stores file information, including file path, file type, upload time, etc.
    """
    __tablename__ = 'file_info'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # File's unique identifier
    filename = Column(String(255), nullable=False)  # Filename
    folder_path = Column(String(255), nullable=False)  # File storage path
    file_extension = Column(String(10), nullable=False)  # Store file extension, length set as needed
    upload_time = Column(DateTime(timezone=True), server_default=func.now())  # Upload time
    knowledge_base_id = Column(String(36), ForeignKey('knowledge_bases.id', ondelete="SET NULL"),
                               nullable=True)  # Optional foreign key associated with KnowledgeBase

    # Establish relationship with KnowledgeBase
    knowledge_base = relationship("KnowledgeBase", back_populates="files")


class DbBase(Base):
    """
    This table stores database configuration information for connecting to multiple database instances.
    """
    __tablename__ = 'db_configs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    database_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())  # Automatically generate creation time


class MessageModel(Base):
    """
    This table stores message records related to conversation threads, including user questions, agent responses, and message types.
    """
    __tablename__ = 'messages'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String(255), ForeignKey('threads.id'))  # Foreign key associated with ThreadModel
    question = Column(Text)  # Message sender's identifier (e.g., 'user', 'agent', etc.)
    response = Column(Text)  # Message content
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Message creation time automatically generated

    message_type = Column(String(255))  # Message type, e.g., 'chat', 'python', 'sql', etc.
    run_result = Column(Text, nullable=True)  # Execution result, can be used to store code execution or command output, this field can be empty

    knowledge_id = Column(String(36))
    knowledge_name = Column(String(255))
    db_id = Column(String(255))
    db_name = Column(String(255))

    # Reverse relationship, can directly access all messages through ThreadModel
    thread = relationship("ThreadModel", back_populates="messages")



