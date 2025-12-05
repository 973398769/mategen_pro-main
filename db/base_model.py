import uuid
from sqlalchemy import create_engine, Column, String, ForeignKey, DateTime, Text, Integer, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from db.base import Base


class SecretModel(Base):
    """
    该表存储代理信息，包括代理的 ID、API 密钥、用户 ID 等字段。
    """
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 自增 ID
    assis_id = Column(String(255), unique=True, nullable=False)  # 存储assistant对象ID
    api_key = Column(String(768), unique=True, nullable=False)  # 限制 api_key 必须唯一
    user_id = Column(String(255), unique=True, nullable=False)  # 新增用户 ID 字段

    initialized = Column(Boolean, default=False)  # 默认值为 false，判断是否执行过初始化
    agent_type = Column(String(255), default="normal")  # 默认值为 "normal"

    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 自动生成创建时间
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 消息更新时间

    threads = relationship("ThreadModel", back_populates="agent", cascade="all, delete-orphan")


class ThreadModel(Base):
    """
    该表存储会话线程的信息，每个线程关联一个代理，并可能包含多个消息和知识库。
    """
    __tablename__ = 'threads'
    id = Column(String(255), primary_key=True)
    agent_id = Column(String(255), ForeignKey('agents.assis_id'))
    conversation_name = Column(String(255))
    run_mode = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())  # 消息更新时间

    # 反向关系到 MessageModel
    messages = relationship("MessageModel", back_populates="thread", order_by="MessageModel.created_at")

    # 其他的关系定义
    knowledge_bases = relationship("KnowledgeBase", back_populates="thread")
    agent = relationship("SecretModel", back_populates="threads")


class KnowledgeBase(Base):
    """
    该表存储知识库的信息，包括知识库名称、分块策略、描述等。
    """
    __tablename__ = 'knowledge_bases'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    # 主键字段
    vector_store_id = Column(String(255), nullable=True)
    # 添加关于文本分块的策略
    chunking_strategy = Column(String(255), default="auto")
    max_chunk_size_tokens = Column(Integer, default=800)
    chunk_overlap_tokens = Column(Integer, default=400)

    # 知识库的名称
    knowledge_base_name = Column(String(255), nullable=False)

    # 新增字段：记录创建时间
    created_at = Column(DateTime, default=func.now())
    # 显示的知识库名称
    display_knowledge_base_name = Column(String(255), nullable=False)
    # 知识库描述
    knowledge_base_description = Column(Text, nullable=True)
    # 外键字段，链接到 threads 表的 id 字段
    thread_id = Column(String(255), ForeignKey('threads.id'))
    # 建立与 ThreadModel 的关系
    thread = relationship("ThreadModel", back_populates="knowledge_bases")
    files = relationship("FileInfo", back_populates="knowledge_base")  # 文件关系


class FileInfo(Base):
    """
    该表存储文件信息，包括文件路径、文件类型和上传时间等。
    """
    __tablename__ = 'file_info'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))  # 文件的唯一标识符
    filename = Column(String(255), nullable=False)  # 文件名
    folder_path = Column(String(255), nullable=False)  # 文件存储路径
    file_extension = Column(String(10), nullable=False)  # 存储文件后缀，长度自行设定
    upload_time = Column(DateTime(timezone=True), server_default=func.now())  # 上传时间
    knowledge_base_id = Column(String(36), ForeignKey('knowledge_bases.id', ondelete="SET NULL"),
                               nullable=True)  # 可选外键关联到KnowledgeBase

    # 建立与KnowledgeBase的关系
    knowledge_base = relationship("KnowledgeBase", back_populates="files")


class DbBase(Base):
    """
    该表存储数据库配置信息，用于连接多个数据库实例。
    """
    __tablename__ = 'db_configs'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    hostname = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    database_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())  # 自动生成创建时间


class MessageModel(Base):
    """
    该表存储与对话线程相关的消息记录，包括用户的问题、代理的响应及消息类型。
    """
    __tablename__ = 'messages'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    thread_id = Column(String(255), ForeignKey('threads.id'))  # 外键关联到 ThreadModel
    question = Column(Text)  # 消息发送者的标识（例如 'user', 'agent' 等）
    response = Column(Text)  # 消息内容
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # 消息创建时间自动生成

    message_type = Column(String(255))  # 消息类型，例如 'chat', 'python', 'sql'等
    run_result = Column(Text, nullable=True)  # 执行结果，可用于存储代码执行或命令的输出，此字段可以为空

    knowledge_id = Column(String(36))
    knowledge_name = Column(String(255))
    db_id = Column(String(255))
    db_name = Column(String(255))

    # 反向关系，可以通过 ThreadModel 直接访问其所有消息
    thread = relationship("ThreadModel", back_populates="messages")



