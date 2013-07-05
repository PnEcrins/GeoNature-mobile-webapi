

CREATE SCHEMA synchronomade;

CREATE TABLE synchronomade.erreurs_cf (
    id serial,
    json text,
    date_import date
);
ALTER TABLE synchronomade.erreurs_cf ADD PRIMARY KEY (id);


CREATE TABLE synchronomade.erreurs_mortalite(
    id serial,
    json text,
    date_import date
);
ALTER TABLE synchronomade.erreurs_mortalite ADD PRIMARY KEY (id);

CREATE TABLE synchronomade.erreurs_inv(
    id serial,
    json text,
    date_import date
);
ALTER TABLE synchronomade.erreurs_inv ADD PRIMARY KEY (id);

