SELECT PLAYER, RANK, AST FROM `prj-gradient-omar.nba_ds.nba_tb`
WHERE Year = '2023-24' AND
  RANK <= 50 AND
  AST > 5
ORDER BY
  RANK ASC
