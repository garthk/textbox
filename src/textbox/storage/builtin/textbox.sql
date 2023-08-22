CREATE TABLE
    "text" (
        [captured] TEXT NOT NULL,
        [uri] TEXT NOT NULL,
        [content] TEXT NOT NULL,
        [metadata] TEXT,
        PRIMARY KEY ([uri], [captured])
    );
