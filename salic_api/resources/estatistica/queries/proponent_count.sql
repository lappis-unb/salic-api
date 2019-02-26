SELECT interessado.Uf, COUNT(DISTINCT projetos.CgcCpf)
FROM SAC.dbo.Projetos as projetos
     INNER JOIN SAC.dbo.Interessado as interessado
              On projetos.CgcCPf = interessado.CgcCpf
       INNER JOIN SAC.dbo.Captacao as capt
              ON (capt.AnoProjeto = projetos.AnoProjeto AND capt.Sequencial = projetos.Sequencial)
              WHERE CaptacaoReal > 0
              GROUP BY interessado.Uf