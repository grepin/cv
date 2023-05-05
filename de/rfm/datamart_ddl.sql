drop table if exists analysis.dm_rfm_segments;

create table if not exists analysis.dm_rfm_segments (
	user_id int4,
	recency SMALLINT CHECK (recency >= 1 AND recency <= 5),
	frequency SMALLINT CHECK (frequency >= 1 AND frequency <= 5),
	monetary_value SMALLINT CHECK (monetary_value >= 1 AND monetary_value <= 5)
)
;

create table if not exists analysis.tmp_rfm_recency (
 user_id INT NOT NULL PRIMARY KEY,
 recency INT NOT NULL CHECK(recency >= 1 AND recency <= 5)
);

create table if not exists analysis.tmp_rfm_frequency (
 user_id INT NOT NULL PRIMARY KEY,
 frequency INT NOT NULL CHECK(frequency >= 1 AND frequency <= 5)
);

create table if not exists analysis.tmp_rfm_monetary_value (
 user_id INT NOT NULL PRIMARY KEY,
 monetary_value INT NOT NULL CHECK(monetary_value >= 1 AND monetary_value <= 5)
);