---
name: curso-whatsapp-acompanhamento
description: >
  Acompanha a campanha de divulgação do curso gratuito no WhatsApp: busca gasto, alcance, conversas
  iniciadas e custo por conversa, cruza com as inscrições que o usuário informar e diz em linguagem
  simples se está indo bem e o que fazer (esperar, trocar imagem, ajustar orçamento). Nunca altera
  nada sem confirmação. Use quando o usuário disser "como está o anúncio", "resultados do curso",
  "quantas mensagens vieram", "vale a pena continuar", "acompanhar a campanha".
---

# Curso Gratuito no WhatsApp. Acompanhamento

Você lê os resultados da campanha do curso e responde três perguntas, nesta ordem:
**quanto gastou, quantas conversas trouxe, e o que fazer agora.** Linguagem simples, números em reais.

**Princípios:**
1. **Ler não custa nada; mudar precisa de SIM.** Pausar, trocar imagem ou mexer em orçamento só
   com confirmação, mostrando o antes e o depois.
2. **Preferir leitura que não gasta cota.** O conector oficial da Meta já permite **ler** a conta do
   Instituto (`is_queryable: true`) mesmo sem liberação para criar. Usar ele para relatórios e
   deixar as ações do Adspirer para criação.
3. **Só a conta do Instituto.** Nunca ler nem mostrar dados da conta pessoal.
4. **Não julgar cedo.** Nos primeiros 3 a 4 dias a Meta está aprendendo. Antes disso, só informar.

---

## Passo 0. Achar a campanha

1. Ler `meus-cursos/*/campanha.yaml`. Se houver mais de um curso, perguntar qual.
2. Sem arquivo: listar as campanhas ativas ou pausadas da conta Instituto BZN e perguntar qual é.

Caminho de leitura, em ordem de preferência:

| Disponível | Usar |
|---|---|
| Conector da Meta (`ads_get_ad_entities`) com a conta do Instituto `is_queryable: true` | conector da Meta, `level: campaign`, filtrando pelo `campaign_id` |
| Senão | Adspirer, `get_meta_campaign_performance` |

No conector da Meta, confirmar os nomes dos campos com `ads_get_field_context` antes de pedir
métricas, e seguir as `next_actions` que a resposta trouxer.

## Passo 1. Buscar os números

Período padrão: desde o início da campanha. Pedir:

- valor gasto
- alcance e impressões
- frequência (quantas vezes, em média, cada pessoa viu)
- cliques no link / taxa de cliques (CTR)
- **conversas iniciadas no WhatsApp** (resultado da campanha) e **custo por conversa**

Se houver mais de um anúncio ou mais de um texto, pedir também por anúncio, para saber qual funciona melhor.

## Passo 2. Perguntar as inscrições

A Meta não sabe quantas pessoas se inscreveram de fato. Perguntar:

```
Das conversas que chegaram no WhatsApp, quantas pessoas se inscreveram no curso até agora?
(se não souber, responda "não sei")
```

Com o número: calcular **% de conversas que viraram inscrição** e **custo por inscrição**
(gasto ÷ inscrições).

## Passo 3. Diagnóstico

Comparar com a **semana anterior** e com a **primeira semana** da própria campanha (gravadas no
histórico). Não usar números de mercado inventados. Regras:

| Sinal | Leitura | Sugestão |
|---|---|---|
| Menos de 4 dias no ar | aprendizado | esperar, não mexer |
| Custo por conversa caiu ou estável | indo bem | manter; se sobrar vaga no curso, considerar subir o orçamento em até 20% |
| Custo por conversa subiu mais de 30% em relação à semana anterior | cansaço ou público saturado | trocar a imagem ou testar novo texto |
| Frequência acima de 3 | as mesmas pessoas estão vendo demais | ampliar o raio ou trocar a imagem |
| Muitos cliques e poucas conversas | a pessoa abre e desiste | revisar a mensagem de boas-vindas e as perguntas rápidas |
| Muitas conversas e poucas inscrições (menos de 1 em cada 5) | problema no atendimento, não no anúncio | responder mais rápido, mandar o link/passo a passo da inscrição logo na primeira resposta |
| Vagas do curso preenchidas | objetivo cumprido | sugerir pausar para não gastar à toa |

## Passo 4. Entregar

Formato curto:

```
CURSO {nome}: dia {n} de {total}

Gasto até agora: R$ {x} (de R$ {previsto})
Conversas no WhatsApp: {n} (R$ {custo} por conversa)
Inscrições: {n} ({pct}% das conversas, R$ {custo} por inscrição)

Situação: {uma frase}

O que eu sugiro:
1. {ação}
2. {ação, se houver}

Quer que eu faça alguma dessas mudanças? (digite o número, ou "não")
```

Qualquer mudança: mostrar o antes e o depois, pedir `SIM`, executar pelo caminho de criação
(o conector da Meta só se a conta estiver liberada nele; senão, Adspirer).

## Passo 5. Registrar

Acrescentar uma linha em `meus-cursos/{slug}/acompanhamento.md`:

```
| 2026-10-01 | dia 4 | gasto R$ 80 | 42 conversas | R$ 1,90/conversa | 9 inscrições | sugestão: manter |
```

Esse histórico é a base da comparação da próxima vez.
