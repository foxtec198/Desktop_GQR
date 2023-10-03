-- select
--     count(Es.Descricao)
-- from 
--     Estrutura Es
-- WHERE
--     Es.HierarquiaDescricao LIKE '%/007864 - FIEP/098629 - FIEP/13223 - PR - LPG - FIEP - LOTE 3/SESI SENAI - MARINGA ZONA 05/%'

select top 10
T.Nome as Tarefa,
R.Nome as Colaborador,
P.Descricao as Pergunta,
E.Conteudo as Resposta,
T.TerminoReal as 'Data Finalização'
from Tarefa T with(nolock)
inner join Recurso R with(nolock)
on T.FinalizadoPorHash = R.CodigoHash
inner join Execucao E with(nolock)
on T.Id = E.TarefaId
inner join Pergunta P with(nolock)
on P.Id = E.PerguntaId
where T.TerminoReal >= '2023-09-19' 
and T.TerminoReal <= '2023-09-23'
and T.EstruturaHierarquiaDescricao like '%31360 - PR - POR - C. VALE%'
