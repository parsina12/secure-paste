from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse, FileResponse
from sqlalchemy.orm import Session
import os

from .database import SessionLocal, init_db
from .models import Paste, FilePaste
from .encryption import encrypt_text, decrypt_text
from .utils import generate_short_id

app = FastAPI()
init_db()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Paste API
@app.post("/paste")
def create_paste(content: str = Form(...), db: Session = next(get_db())):
    iv, ciphertext = encrypt_text(content)
    short_id = generate_short_id()
    paste = Paste(short_id=short_id, iv=iv, ciphertext=ciphertext)
    db.add(paste)
    db.commit()
    db.refresh(paste)
    return {"url": f"/paste/{short_id}"}

@app.get("/paste/{short_id}")
def get_paste(short_id: str, db: Session = next(get_db())):
    paste = db.query(Paste).filter(Paste.short_id == short_id).first()
    if paste:
        plain = decrypt_text(paste.iv, paste.ciphertext)
        return JSONResponse(content={"content": plain})
    else:
        raise HTTPException(404, "Paste not found")

# File Upload API
@app.post("/file")
async def upload_file(file: UploadFile = File(...), db: Session = next(get_db())):
    data = await file.read()
    iv, ciphertext = encrypt_text(data.decode(errors="ignore"))  # for demo; for binary, use custom
    short_id = generate_short_id()
    fp = FilePaste(short_id=short_id, filename=file.filename, iv=iv, ciphertext=ciphertext)
    db.add(fp)
    db.commit()
    db.refresh(fp)
    return {"url": f"/file/{short_id}"}

@app.get("/file/{short_id}")
def download_file(short_id: str, db: Session = next(get_db())):
    fp = db.query(FilePaste).filter(FilePaste.short_id == short_id).first()
    if fp:
        content = decrypt_text(fp.iv, fp.ciphertext)
        filepath = os.path.join(UPLOAD_DIR, fp.filename)
        with open(filepath, "wb") as f:
            f.write(content.encode())
        return FileResponse(filepath, filename=fp.filename)
    else:
        raise HTTPException(404, "File not found")
