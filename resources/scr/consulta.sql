select T.Nome, R.Nome, T.TerminoReal
from Tarefa T with(nolock)
join Recurso R with(nolock)
on R.CodigoHash = T.FinalizadoPorHash
where T.TerminoReal >= '2023-10-11'
and T.EstruturaHierarquiaDescricao LIKE '%42636%'
and T.ServicoDescricao LIKE 'CONTROLE DE ACESSO'
order by T.TerminoReal DESC