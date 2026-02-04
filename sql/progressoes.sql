select 
    fw.C093_NUMERO as cm, 
    (
        SELECT DISTINCT ON (C093_COD)
            FPC061_DESCR
        FROM
            FPC228 as progs
            left join FPC061 ON FPC061.FPC061_COD = progs.FPC061_COD
        WHERE
            progs.C093_COD = fw.C093_COD and
            FPC255_COD in (1, 13) -- prog vert e vert esp
        ORDER BY
            C093_COD,
            FPC228_DATA  DESC, -- mais recente
            progs.FPC061_COD DESC -- seleciona especial caso haja
    ) as nivel_atual,
    (
        SELECT DISTINCT ON (C093_COD)
            FPC060_DESCR
        FROM
            FPC228 as progs
            left join FPC060 ON FPC060.FPC060_COD = progs.FPC060_COD
        WHERE
            progs.C093_COD = fw.C093_COD
        ORDER BY
            C093_COD,
            FPC060.FPC060_COD DESC -- maior letra
    ) as letras_adquiridas
    
from VW_FUNCIONARIOS_WEB fw

where FPC104_NUMERO IN (1,3, 13) -- efetivos fufin e bhprev
    and FPC011_RESCISAO is null