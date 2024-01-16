select * from Tarefa t
inner join dw_vista.dbo.DM_Estrutura es on es.Id_Estrutura = t.EstruturaId
where month(terminoreal) = 01 
and  year(terminoreal) = 2024
and Nome = 'Visita Oper. Liderança'
and es.crno = 49454