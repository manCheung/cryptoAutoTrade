CREATE TABLE IF NOT EXISTS crypto_bot.prices (
	id serial NOT NULL,
	symbol VARCHAR(30),
	symbol_id VARCHAR(100),
	price float8,
	total_volumn bigint,
	market_cap bigint,
	market_cap_rank int,
	high_24h float8,
	low_24h float8,
	price_change_24h float8,
	price_change_percentage_24h float8,
	datetime timestamp(3) with time zone NOT NULL,
	epoch_time int NOT NULL,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS crypto_bot.history (
	id serial NOT NULL,
	symbol_id VARCHAR(100) NOT NULL,
	amount float8 NOT NULL,
	address VARCHAR(255) NOT NULL,
  	current_price float8 NOT NULL,
  	action_type int NOT NULL,
	gas float8 NOT NULL,
	gas_price float8 NOT NULL,
	datetime timestamp(3) with time zone NOT NULL,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS crypto_bot.types (
	id serial NOT NULL,
	type_key VARCHAR(50) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS crypto_bot.settings (
	id serial NOT NULL,
	up_monitor_minutes int NOT NULL,
	down_monitor_minutes int NOT NULL,
	up_precentage int NOT NULL,
  	down_precentage int NOT NULL,
  	gas int NOT NULL,
  	gas_price int NOT NULL,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS crypto_bot.excluded_token (
	id serial NOT NULL,
	symbol_id VARCHAR(100) NOT NULL,
	address VARCHAR(255) NOT NULL,
	PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS crypto_bot.latest_prices (
	id serial NOT NULL,
	symbol VARCHAR(30),
	symbol_id VARCHAR(100),
	price float8,
	total_volumn bigint,
	market_cap bigint,
	market_cap_rank int,
	high_24h float8,
	low_24h float8,
	price_change_24h float8,
	price_change_percentage_24h float8,
	datetime timestamp(3) with time zone NOT NULL,
	epoch_time int NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS crypto_bot.wallet (
	id serial NOT NULL,
	symbol_id VARCHAR(100),
	address VARCHAR(255),
	price float8,
	amount float8,
	datetime timestamp(3) with time zone NOT NULL,
	PRIMARY KEY (id)
)