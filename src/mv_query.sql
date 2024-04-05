DROP VIEW IF EXISTS summaries;
CREATE VIEW summaries AS
SELECT window_start, window_end, location, COUNT(*) as transaction_count, SUM(amount) as total_amount
FROM TABLE(TUMBLE(TABLE atm_demo_trans, DESCRIPTOR(eventTimestamp), INTERVAL '5' MINUTES))
GROUP BY window_start, window_end, location
;
SELECT * FROM summaries
;

