SELECT
Es.QRCode,
Es.Descricao,
Es.Id,
(SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
FROM Estrutura ES
INNER JOIN DW_Vista.dbo.DM_ESTRUTURA DE ON DE.ID_Estrutura = ES.Id
WHERE DE.Nivel_03 = '60433 - PR - POR - COND SPAZIO LEOPOLDINA'
AND Es.Tipo = 'L'
AND Es.Nivel = 3