SELECT interessado.Uf, SUM(Aprovado)
FROM SAC.dbo.Projetos as projetos
INNER JOIN SAC.dbo.interessado as interessado
ON interessado.CgcCpf = projetos.CgcCpf
INNER JOIN SAC.dbo.vAprovadoCaptado as aprovado
ON (aprovado.AnoProjeto = projetos.AnoProjeto AND aprovado.Sequencial = projetos.Sequencial)
WHERE Captado > 0
GROUP BY interessado.Uf;