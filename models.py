from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class WatchedVideo(Base):
    __tablename__ = 'watched_videos'
    id = Column(String, primary_key=True)  # ID gerado via UUID do vídeo
    curso_id = Column(String)

# Configuração do banco
engine = create_engine('sqlite:///watched.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
