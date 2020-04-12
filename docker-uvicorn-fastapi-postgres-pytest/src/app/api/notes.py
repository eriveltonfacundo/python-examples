from typing import List
from app.repository import notes_repository
from app.repository.models import NoteDB, NoteSchema
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payload: NoteSchema):
    note_id = await notes_repository.post(payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int = Path(..., gt=0)):
    note = await notes_repository.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await notes_repository.get_all()


@router.put("/{id}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, id: int = Path(..., gt=0)):
    note = await notes_repository.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await notes_repository.put(id, payload)

    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=NoteDB)
async def delete_note(id: int = Path(..., gt=0)):
    note = await notes_repository.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await notes_repository.delete(id)

    return note
