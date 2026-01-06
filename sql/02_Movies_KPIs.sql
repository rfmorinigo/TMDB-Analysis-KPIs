-- KPI 1: Películas con mayor Retorno sobre la Inversión (ROI)
-- -----------------------------------------------------------
-- Pregunta de negocio:
-- ¿Qué películas generaron mayor rentabilidad en relación con su presupuesto?
--
-- Definición:
-- El ROI (Return on Investment) se calcula como:
-- (revenue - budget) / budget
--
-- Criterios de limpieza aplicados:
-- - Se consideran solo películas con presupuesto mayor a 0
-- - Se consideran solo películas con recaudación mayor a 0
-- - Se excluyen valores nulos
--
-- Propósito:
-- Este KPI permite identificar producciones altamente eficientes desde el punto
-- de vista financiero, independientemente de su recaudación absoluta.
--
-- Notas:
-- - El ROI se redondea a dos decimales para facilitar la lectura y el análisis.

SELECT
    m.movie_id,
    m.title,
    m.release_date,
    m.popularity,
    m.vote_average,
    m.vote_count,
    m.budget,
    m.revenue,
    ROUND((m.revenue - m.budget) * 1.0 / m.budget, 2) AS roi
FROM movies m
WHERE m.budget IS NOT NULL
  AND m.budget > 0
  AND m.revenue IS NOT NULL
  AND m.revenue > 0
ORDER BY roi DESC
LIMIT 10;


-- KPI 2: Retorno sobre la Inversión (ROI) promedio por género
-- ----------------------------------------------------------
-- Pregunta de negocio:
-- ¿Qué géneros cinematográficos presentan, en promedio, mayor rentabilidad
-- en relación con el presupuesto invertido?
--
-- Definición:
-- El ROI promedio por género se calcula como el promedio del ROI individual
-- de las películas asociadas a cada género.
--
-- Criterios de limpieza aplicados:
-- - Se consideran solo películas con presupuesto mayor a 0
-- - Se consideran solo películas con recaudación mayor a 0
-- - Se excluyen valores nulos
--
-- Consideraciones del modelo:
-- - Una película puede pertenecer a múltiples géneros.
-- - En estos casos, la película contribuye al promedio de cada género asociado.
--
-- Propósito:
-- Este KPI permite identificar géneros que, en términos generales, ofrecen
-- mejores retornos de inversión, aportando información relevante para la toma
-- de decisiones estratégicas y de inversión.
--
-- Notas:
-- - El ROI se calcula a nivel película y luego se promedia por género.
-- - Los valores de ROI se redondean para facilitar la interpretación.

SELECT
    g.genre_name,
    ROUND(
        AVG(
            (m.revenue - m.budget) * 1.0 / m.budget
        ),
        2
    ) AS avg_roi
FROM genres g
JOIN movie_genres mg 
    ON mg.genre_id = g.genre_id
JOIN movies m 
    ON m.movie_id = mg.movie_id
WHERE m.budget IS NOT NULL
  AND m.budget > 0
  AND m.revenue IS NOT NULL
  AND m.revenue > 0
GROUP BY g.genre_name
ORDER BY avg_roi DESC;


-- KPI 3: Películas rentables con buena valoración del público
-- -----------------------------------------------------------
-- Pregunta de negocio:
-- ¿Qué películas lograron combinar una alta rentabilidad financiera
-- con una buena recepción por parte del público?
--
-- Métricas utilizadas:
-- - Retorno sobre la Inversión (ROI)
-- - Calificación promedio del público (vote_average)
-- - Cantidad de votos (vote_count) > 5000
--
-- Criterios de limpieza aplicados:
-- - Presupuesto mayor a 0
-- - Recaudación mayor a 0
--
-- Propósito:
-- Este KPI permite identificar producciones exitosas tanto desde el
-- punto de vista financiero como de percepción de calidad, aportando
-- información clave para decisiones estratégicas de inversión.

SELECT
    m.title,
    m.release_date,
    m.vote_average,
    m.vote_count,
    m.budget,
    m.revenue,
    ROUND((m.revenue - m.budget) * 1.0 / m.budget,2) AS roi
FROM movies m
WHERE m.budget IS NOT NULL
  AND m.budget > 0
  AND m.revenue IS NOT NULL
  AND m.revenue > 0
  AND m.vote_average >= 7
  AND m.vote_count > 5000
ORDER BY roi DESC, m.vote_average DESC
LIMIT 10; 

-- KPI 4: Distribución de popularidad por género
-- ---------------------------------------------
-- Mide la participación de cada género en la demanda total
-- del público, utilizando la suma de popularidad.

SELECT
    g.genre_name,
    ROUND(SUM(m.popularity), 2) AS total_popularity,
    COUNT(DISTINCT m.movie_id) AS total_movies
FROM genres g
JOIN movie_genres mg 
    ON mg.genre_id = g.genre_id
JOIN movies m 
    ON m.movie_id = mg.movie_id
WHERE m.popularity IS NOT NULL
GROUP BY g.genre_name
ORDER BY total_popularity DESC;
 