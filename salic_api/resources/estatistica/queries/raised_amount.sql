SELECT interessado.Uf, SUM(CaptacaoReal)
FROM SAC.dbo.Projetos as projetos
     INNER JOIN SAC.dbo.Interessado as interessado
              ON interessado.CgcCpf = projetos.CgcCpf
       INNER JOIN SAC.dbo.Captacao as capt
              ON (capt.AnoProjeto = projetos.AnoProjeto AND capt.Sequencial = projetos.Sequencial)
GROUP BY interessado.Uf;

