# Meus cursos

Aqui ficam os arquivos que as skills de divulgação guardam para cada curso, um por pasta:

```
meus-cursos/
  informatica-basica/
    curso.yaml           dados do curso (nome, datas, local, público)
    campanha.yaml        campanha criada no Meta (IDs, orçamento, status)
    acompanhamento.md    histórico dos resultados, dia a dia
```

Você não precisa mexer neles. As skills criam e atualizam esses arquivos.

## Como usar

| Quando | Comando |
|---|---|
| Criar o anúncio de um curso novo | `/curso-whatsapp-campanha` |
| Ver como o anúncio está indo | `/curso-whatsapp-acompanhamento` |

Adaptado do "Pacote Lançamento Pago" para o caso de curso gratuito com conversas no WhatsApp:
sem pixel, sem Hotmart e sem token, usando o Adspirer (e o conector oficial da Meta quando ele
estiver liberado para a conta do Instituto).
