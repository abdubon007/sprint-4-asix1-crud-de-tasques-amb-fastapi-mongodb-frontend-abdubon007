import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient, ReturnDocument
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------------ #
#                        Inicialització de l'aplicació                     #
# ------------------------------------------------------------------------ #

app = FastAPI(
    title="Gestor de Llibres API",
    summary="API REST amb FastAPI i MongoDB per gestionar llibres",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------------------------ #
#                     Configuració connexió MongoDB                        #
# ------------------------------------------------------------------------ #

client = AsyncMongoClient(os.environ["MONGODB_URL"])
db = client.sprint4
book_collection = db.get_collection("books")

PyObjectId = Annotated[str, BeforeValidator(str)]

# ------------------------------------------------------------------------ #
#                          Definició dels models                           #
# ------------------------------------------------------------------------ #

class BookModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    autor: str = Field(...)
    estat: str = Field(default="pendent")       # pendent / llegit
    valoracio: int = Field(default=1, ge=1, le=5)  # 1 - 5
    categoria: str = Field(default="general")
    persona: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "El Senyor dels Anells",
                "autor": "J.R.R. Tolkien",
                "estat": "pendent",
                "valoracio": 5,
                "categoria": "fantasia",
                "persona": "Abdullah"
            }
        },
    )


class UpdateBookModel(BaseModel):
    titol: Optional[str] = None
    autor: Optional[str] = None
    estat: Optional[str] = None
    valoracio: Optional[int] = None
    categoria: Optional[str] = None
    persona: Optional[str] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "estat": "llegit",
                "valoracio": 4
            }
        },
    )


class BookCollection(BaseModel):
    books: List[BookModel]


# ------------------------------------------------------------------------ #
#                         Endpoints CRUD + Filtres                         #
# ------------------------------------------------------------------------ #

# ── CREATE ───────────────────────────────────────────────────────────────

@app.post(
    "/books/",
    response_model=BookModel,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nou llibre",
)
async def create_book(book: BookModel):
    new_book = await book_collection.insert_one(
        book.model_dump(by_alias=True, exclude=["id"])
    )
    created_book = await book_collection.find_one({"_id": new_book.inserted_id})
    return created_book


# ── READ ALL ─────────────────────────────────────────────────────────────

@app.get(
    "/books/",
    response_model=BookCollection,
    summary="Llistar tots els llibres",
)
async def list_books():
    return BookCollection(books=await book_collection.find().to_list(1000))


# ── READ BY ID ───────────────────────────────────────────────────────────

@app.get(
    "/books/{id}",
    response_model=BookModel,
    summary="Obtenir un llibre per ID",
)
async def show_book(id: str):
    book = await book_collection.find_one({"_id": ObjectId(id)})
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Llibre amb ID '{id}' no trobat"
        )
    return book


# ── UPDATE ───────────────────────────────────────────────────────────────

@app.put(
    "/books/{id}",
    response_model=BookModel,
    summary="Actualitzar un llibre existent",
)
async def update_book(id: str, book: UpdateBookModel):
    book_data = {k: v for k, v in book.model_dump().items() if v is not None}

    if len(book_data) >= 1:
        updated = await book_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": book_data},
            return_document=ReturnDocument.AFTER,
        )
        if updated is not None:
            return updated

    existing = await book_collection.find_one({"_id": ObjectId(id)})
    if existing is not None:
        return existing

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Llibre amb ID '{id}' no trobat"
    )


# ── DELETE ───────────────────────────────────────────────────────────────

@app.delete(
    "/books/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un llibre",
)
async def delete_book(id: str):
    result = await book_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count != 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Llibre amb ID '{id}' no trobat"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
