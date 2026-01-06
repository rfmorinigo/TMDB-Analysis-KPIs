 -- Cleaning rules for financial analysis
-- Movies must have:
-- - budget > 0
-- - revenue > 0
-- - non-null values

SELECT *
FROM movies
WHERE budget IS NOT NULL
  AND budget > 0
  AND revenue IS NOT NULL
  AND revenue > 0;
