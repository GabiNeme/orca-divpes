-- Obtém nome, progressão horizontal máxima e tempo sem efetivo exercício

select 
    fw.C093_NUMERO as cm, 
    fw.C000_RAZAO as nome,

    (select sum(QTDE_DIAS)
    FROM VW_AFASTAMENTOS
    WHERE 
        FPC013_COD in (8, 9, 18, 26, 33, 37, 44, 57) -- licenças que interrompem progressao
        and VW_AFASTAMENTOS.C093_COD = fw.C093_COD
    GROUP BY VW_AFASTAMENTOS.C093_COD) as qtde_dias_licenca,
    (
        SELECT DISTINCT ON (C093_COD)
            FPC060_DESCR
        FROM
            FPC228 as progs
            left join FPC060 ON FPC060.FPC060_COD = progs.FPC060_COD
        WHERE
            progs.C093_COD = fw.C093_COD and
            FPC255_COD in (2, 3, 5, 14) -- prog hor, chefia, lanç futuro e hor esp
        ORDER BY
            C093_COD,
            FPC228_DATA  DESC, -- mais recente
            FPC060.FPC060_DESCR DESC -- seleciona maior se a data for a mesma
    ) as letra_maxima
    
from VW_FUNCIONARIOS_WEB fw

where FPC104_NUMERO IN (1,3, 13) -- efetivos fufin e bhprev
    and FPC011_RESCISAO is null