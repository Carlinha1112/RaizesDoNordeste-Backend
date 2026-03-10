from src.infrastructure.database.database import engine, Base
from src.domain.entities import *

Base.metadata.create_all(bind=engine)