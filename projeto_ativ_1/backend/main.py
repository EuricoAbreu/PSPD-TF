from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# from pydantic import BaseSettings, PostgresDsn
from pydantic_settings import BaseSettings
import base64

class DatabaseConfig(BaseSettings):
    user: str
    password: str
    host: str
    port: int = 5432 
    dbname: str

    @property
    def DATABASE_URL(self):
        """Construa a URL de conexão com o PostgreSQL."""
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"

    class Config:
        env_file = ".env"  
        env_file_encoding = 'utf-8'

database_config = DatabaseConfig()
engine = create_engine(database_config.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    format = Column(String, index=True)
    file_data = Column(String)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/upload/")
def upload_image(
    file: UploadFile = File(...),
    name: str = Form(...),
    category: str = Form(...),
    db: Session = Depends(get_db)
):
    file_format = file.filename.split(".")[-1]
    file_data = base64.b64encode(file.file.read()).decode('utf-8')
    
    new_image = Image(name=name, category=category, format=file_format, file_data=file_data)
    db.add(new_image)
    db.commit()
    return {"message": "Image uploaded successfully!"}

@app.get("/images/")
def get_images(category: str = None, name: str = None, db: Session = Depends(get_db)):
    query = db.query(Image)
    if category:
        query = query.filter(Image.category == category)
    if name:
        query = query.filter(Image.name.contains(name))
    return query.all()

@app.get("/image/{image_id}")
def get_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@app.put("/image/{image_id}")
def update_image(image_id: int, name: str = Form(None), category: str = Form(None), file: UploadFile = None, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    if name:
        image.name = name
    if category:
        image.category = category
    if file:
        file_format = file.filename.split(".")[-1]
        image.file_data = base64.b64encode(file.file.read()).decode('utf-8')
        image.format = file_format
    db.commit()
    return {"message": "Image updated successfully!"}

@app.get("/download/{image_id}")
def download_image(image_id: int, db: Session = Depends(get_db)):
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"name": image.name, "format": image.format, "file_data": image.file_data}