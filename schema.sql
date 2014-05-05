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


ALTER TABLE promocodes RENAME COLUMN amount TO bytes;


CREATE TABLE api_keys (
  id  SERIAL,
  key VARCHAR
);
