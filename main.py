"""
Taller: Variables de entorno y conexión de FastAPI con Supabase

La API deja de leer albums.json y habla con la tabla `albums` de Supabase
usando las mismas consultas SQL.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# 1. Cargar variables de entorno desde el archivo .env
load_dotenv()

# 2. Leer la URL de la base de datos (nunca hardcodeada)
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "No se encontró DATABASE_URL.\n"
        "1. Copia .env.example a .env\n"
        "2. Pon tu connection string de Supabase (con la contraseña real)"
    )

# 3. Crear el motor de conexión
engine = create_engine(DATABASE_URL)

app = FastAPI(
    title="API de Álbumes (Supabase)",
    description="Conexión a la tabla albums usando variables de entorno",
    version="1.0.0"
)


# ---------- Modelos ----------
class Album(BaseModel):
    id: Optional[int] = None
    titulo: str
    artista: str
    anio: Optional[int] = None
    genero: Optional[str] = None


class AlbumCreate(BaseModel):
    titulo: str
    artista: str
    anio: Optional[int] = None
    genero: Optional[str] = None


# ---------- Endpoints ----------
@app.get("/")
def root():
    return {
        "mensaje": "API de Álbumes conectada a Supabase",
        "endpoints": ["/albums", "/albums/{id}"]
    }


@app.get("/albums", response_model=List[Album])
def listar_albums():
    """GET /albums - Lee todos los álbumes desde Supabase."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, titulo, artista, anio, genero FROM albums ORDER BY id")
            )
            rows = result.fetchall()
            return [
                Album(id=r.id, titulo=r.titulo, artista=r.artista, anio=r.anio, genero=r.genero)
                for r in rows
            ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {str(e)}")


@app.get("/albums/{album_id}", response_model=Album)
def obtener_album(album_id: int):
    """Obtiene un álbum por su id."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT id, titulo, artista, anio, genero FROM albums WHERE id = :id"),
                {"id": album_id}
            )
            row = result.fetchone()
            if not row:
                raise HTTPException(status_code=404, detail="Álbum no encontrado")
            return Album(id=row.id, titulo=row.titulo, artista=row.artista, anio=row.anio, genero=row.genero)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la base de datos: {str(e)}")


@app.post("/albums", response_model=Album, status_code=201)
def crear_album(album: AlbumCreate):
    """Crea un nuevo álbum en la tabla albums."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("""
                    INSERT INTO albums (titulo, artista, anio, genero)
                    VALUES (:titulo, :artista, :anio, :genero)
                    RETURNING id, titulo, artista, anio, genero
                """),
                {
                    "titulo": album.titulo,
                    "artista": album.artista,
                    "anio": album.anio,
                    "genero": album.genero
                }
            )
            conn.commit()
            row = result.fetchone()
            return Album(id=row.id, titulo=row.titulo, artista=row.artista, anio=row.anio, genero=row.genero)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear el álbum: {str(e)}")


@app.delete("/albums/{album_id}", status_code=204)
def eliminar_album(album_id: int):
    """Elimina un álbum por su id."""
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text("DELETE FROM albums WHERE id = :id RETURNING id"),
                {"id": album_id}
            )
            conn.commit()
            if not result.fetchone():
                raise HTTPException(status_code=404, detail="Álbum no encontrado")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar el álbum: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
