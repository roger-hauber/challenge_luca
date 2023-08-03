-- All my SQL queries from the challenges
-- TASK ONE (for one of the week/month, total/average combos)
SELECT
    SUM(totalAmount) AS total,
    strftime('%W', payments.paymentCreatedAt) AS month

FROM payments
WHERE NOT payments.status = 'ERR'

GROUP BY month


-- TASK TWO
SELECT
    COUNT(totalAmount) AS num_trans,
    city

FROM payments
JOIN locations ON payments.locationId = locations.uuid
WHERE NOT payments.status = "ERR"

GROUP BY city

-- TASK THREE
WITH incl_rank AS
  (SELECT
  SUM(totalAmount) as total,
  AVG(totalAmount) as average,
  MAX(totalAmount),
  locationId,
  city,
  RANK() OVER (
      PARTITION BY city
      ORDER BY city ASC, MAX(totalAmount) DESC
  ) AS order_rank

  FROM payments JOIN locations ON payments.locationId=locations.uuid
  WHERE NOT payments.status = "ERR"
  GROUP BY city, locationId
  ORDER BY city ASC, MAX(totalAmount) DESC)

SELECT *
FROM incl_rank
WHERE order_rank = 2

-- TASK FOUR
SELECT
    AVG(totalAmount) AS average,
    SUM(totalAmount) AS total,
    city,
    strftime("%H", paymentCreatedAt) AS hour

FROM payments JOIN locations ON payments.locationId=locations.uuid
WHERE NOT payments.status = "ERR"

GROUP BY city, hour
