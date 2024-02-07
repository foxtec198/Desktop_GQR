SELECT 
E.Descricao as Nome, 
E.QRCode, 
E.Grupo 
FROM Estrutura E 
INNER JOIN DW_Vista.dbo.DM_Estrutura as Es on Es.Id_Estrutura = Id 
WHERE Es.CRNo = 17739 
AND E.Nivel >= 5