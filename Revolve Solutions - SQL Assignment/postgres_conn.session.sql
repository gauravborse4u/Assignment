
--  Manufacturer's who has most number of flights
SELECT p.manufacturer, COUNT(*) AS flight_count
FROM flights f
JOIN planes p ON f.tailnum = p.tailnum
GROUP BY p.manufacturer
ORDER BY flight_count DESC
LIMIT 1;


-- Manufacturer's who has most no of flying hours
SELECT p.manufacturer, SUM(CAST(f.air_time AS INTEGER)) / 60.0 AS total_flying_hours
FROM flights f
JOIN planes p ON f.tailnum = p.tailnum
WHERE f.air_time <> 'NA'
GROUP BY p.manufacturer
ORDER BY total_flying_hours DESC
LIMIT 1;



--  Plane flew the most number of hours
SELECT
  flights.tailnum AS plane_tailnum,
  SUM(CAST(flights.air_time AS INT)) AS total_flight_hours
FROM
  flights
WHERE
  flights.air_time <> 'NA' -- Exclude 'NA' values
GROUP BY
  flights.tailnum
ORDER BY
  total_flight_hours DESC
LIMIT 1;



-- Destination had most delay in flights
SELECT
  dest AS destination,
  SUM(CAST(arr_delay AS INT)) AS total_delay
FROM
  flights
WHERE
  arr_delay IS NOT NULL
  AND arr_delay <> 'NA' -- Exclude 'NA' values
GROUP BY
  dest
ORDER BY
  total_delay DESC
LIMIT 1;


-- Manufactures planes who had covered most distance
-- It will return if multiple planes who has same maximum distance covered
SELECT
  planes.manufacturer,
  SUM(flights.distance) AS total_distance_covered
FROM
  planes
JOIN
  flights ON planes.tailnum = flights.tailnum
GROUP BY
  planes.manufacturer
HAVING
  SUM(flights.distance) = (
    SELECT
      MAX(total_distance)
    FROM
      (SELECT
        SUM(flights.distance) AS total_distance
      FROM
        planes
      JOIN
        flights ON planes.tailnum = flights.tailnum
      GROUP BY
        planes.manufacturer) AS subquery
  );


-- Airport has most flights on weekends
SELECT f.origin AS airport, COUNT(*) AS weekend_flight_count
FROM flights f
WHERE EXTRACT(ISODOW FROM DATE(f.year::text || '-' || f.month::text || '-' || f.day::text)) IN (6, 7) -- 6 is Saturday, 7 is Sunday
GROUP BY f.origin
ORDER BY weekend_flight_count DESC
LIMIT 1;



