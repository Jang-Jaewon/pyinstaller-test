from sqlalchemy.orm import Session

from app.api.models.file import File


def create_file(file_path: str, host_name: str, db: Session):
    file_obj = File(image_path=file_path, created_by=host_name)
    db.add(file_obj)
    db.commit()
    db.refresh(file_obj)
    return file_obj


def get_files(cursor_id: int, page_size: int, db: Session):
    query = db.query(File).filter(File.deleted_at == None)
    if cursor_id:
        query = query.filter(File.id > cursor_id)
    return query.order_by(File.id).limit(page_size).all()
