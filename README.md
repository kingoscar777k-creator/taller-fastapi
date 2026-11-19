# Taller: Variables de entorno + FastAPI + Supabase

La API deja de leer `albums.json` y habla con la tabla `albums` de Supabase.

---

## Antes de empezar

- [ ] Tienes el proyecto de Supabase `catalogo-albums` con la tabla `albums`
- [ ] Tienes la contraseña de la base de datos (Database → Settings)

---

## Instalación en Windows (Git Bash)

### 1. Abre la carpeta del proyecto

```bash
cd ~/Desktop/taller-fastapi-supabase
```

### 2. Crea el entorno virtual

```bash
python -m venv .venv
```

### 3. Actívalo (¡importante en Windows!)

```bash
source .venv/Scripts/activate
```

Deberías ver `(.venv)` al principio de la línea.

### 4. Actualiza pip e instala las dependencias

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Si `psycopg2-binary` da error, prueba esto:

```bash
pip install psycopg2-binary --only-binary=:all:
pip install -r requirements.txt
```

### 5. Configura las variables de entorno

```bash
cp .env.example .env
```

Abre el archivo `.env` con el bloc de notas o VS Code y pon tu **DATABASE_URL** real de Supabase (con la contraseña).

Ejemplo:
```
DATABASE_URL=postgresql://postgres:mi_password_secreto@db.abcdefghijk.supabase.co:5432/postgres
```

### 6. Arranca la API

```bash
uvicorn main:app --reload
```

Abre en el navegador: http://127.0.0.1:8000/docs

---

## Endpoints disponibles

| Método | Ruta            | Descripción              |
|--------|-----------------|--------------------------|
| GET    | /albums         | Lista todos los álbumes  |
| GET    | /albums/{id}    | Un álbum por id          |
| POST   | /albums         | Crear un álbum nuevo     |
| DELETE | /albums/{id}    | Eliminar un álbum        |

---

## Seguridad

| Archivo        | ¿Se sube a GitHub? | Motivo                     |
|----------------|--------------------|----------------------------|
| `.env.example` | Sí                 | Solo tiene placeholders    |
| `.env`         | **NO**             | Contiene la contraseña     |
| `.gitignore`   | Sí                 | Protege el `.env`          |

---

## Si tus columnas se llaman distinto

Si en Supabase tu tabla tiene columnas como `title`, `artist`, `year`..., cambia las consultas SQL en `main.py` para que coincidan.
