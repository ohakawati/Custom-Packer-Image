WITH player_stats AS (
  SELECT
    Year,
    PLAYER,
    AVG(PTS) AS average_pts,
    AVG(REB) AS average_reb,
    AVG(AST) AS average_ast
  FROM
    `prj-gradient-omar.nba_ds.nba_tb`
  GROUP BY
    Year, PLAYER
),

normalized_stats AS (
  SELECT
    Year,
    PLAYER,
    CASE 
      WHEN MAX(average_pts) OVER (PARTITION BY PLAYER) = MIN(average_pts) OVER (PARTITION BY PLAYER) THEN 1
      ELSE (average_pts - MIN(average_pts) OVER (PARTITION BY PLAYER)) / (MAX(average_pts) OVER (PARTITION BY PLAYER) - MIN(average_pts) OVER (PARTITION BY PLAYER))
    END AS norm_pts,
    CASE 
      WHEN MAX(average_reb) OVER (PARTITION BY PLAYER) = MIN(average_reb) OVER (PARTITION BY PLAYER) THEN 1
      ELSE (average_reb - MIN(average_reb) OVER (PARTITION BY PLAYER)) / (MAX(average_reb) OVER (PARTITION BY PLAYER) - MIN(average_reb) OVER (PARTITION BY PLAYER))
    END AS norm_reb,
    CASE 
      WHEN MAX(average_ast) OVER (PARTITION BY PLAYER) = MIN(average_ast) OVER (PARTITION BY PLAYER) THEN 1
      ELSE (average_ast - MIN(average_ast) OVER (PARTITION BY PLAYER)) / (MAX(average_ast) OVER (PARTITION BY PLAYER) - MIN(average_ast) OVER (PARTITION BY PLAYER))
    END AS norm_ast
  FROM
    player_stats
),

composite_score AS (
  SELECT
    Year,
    PLAYER,
    (norm_pts + norm_reb + norm_ast) / 3 AS improvement_score
  FROM
    normalized_stats
)

SELECT
  Year,
  PLAYER,
  improvement_score
FROM
  composite_score
ORDER BY
  PLAYER, Year