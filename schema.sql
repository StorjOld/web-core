CREATE TABLE promocodes (
  id        SERIAL,
  promocode VARCHAR,
  amount    BIGINT
);

CREATE TABLE promocode_uses (
  id        SERIAL,
  token     VARCHAR,
  promocode VARCHAR
);

CREATE TABLE balances (
  id     SERIAL,
  token  VARCHAR,
  amount BIGINT
);

CREATE TABLE movements (
  id     SERIAL,
  token  VARCHAR,
  amount BIGINT
);

CREATE TABLE prices (
  id     SERIAL,
  bytes  BIGINT,
  amount BIGINT
);

INSERT INTO prices (bytes, amount) VALUES
  ( 100 * 1024 * 1024 * 1024,  500),
  (1000 * 1024 * 1024 * 1024, 5000);

INSERT INTO promocodes (promocode, amount) VALUES
  ('STORJ2014', 500);
