-- Ejecuta esto en el SQL Editor de Supabase si aún no tienes la tabla

CREATE TABLE IF NOT EXISTS albums (
    id SERIAL PRIMARY KEY,
    titulo TEXT NOT NULL,
    artista TEXT NOT NULL,
    anio INTEGER,
    genero TEXT
);

-- Datos de ejemplo (opcional)
INSERT INTO albums (titulo, artista, anio, genero) VALUES
    ('The Dark Side of the Moon', 'Pink Floyd', 1973, 'Rock'),
    ('Abbey Road', 'The Beatles', 1969, 'Rock'),
    ('Thriller', 'Michael Jackson', 1982, 'Pop'),
    ('Nevermind', 'Nirvana', 1991, 'Grunge'),
    ('Kind of Blue', 'Miles Davis', 1959, 'Jazz');
