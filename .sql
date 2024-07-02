SELECT
Es.QRCode,
Es.Descricao,
Es.Id,
(SELECT Descricao FROM Estrutura Es2 WHERE Es2.Id = Es.EstruturaSuperiorId) as 'Superior'
FROM Estrutura ES
WHERE Es.HierarquiaDescricao LIKE '%34364 -%'
AND Es.Tipo = 'L'
AND Es.Nivel >= 4