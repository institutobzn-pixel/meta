---
name: curso-whatsapp-campanha
description: >
  Cria, do zero, uma campanha de Engajamento no Meta Ads (Facebook + Instagram) que leva as pessoas
  para uma conversa no WhatsApp do Instituto, para divulgar um curso gratuito. Conduz uma pergunta por
  vez: dados do curso, público, orçamento, imagem e mensagem de boas-vindas. Escreve os textos,
  mostra o resumo completo, pede confirmação e cria tudo PAUSADO, pelo Adspirer (ou pelo conector
  oficial da Meta, quando a conta estiver liberada nele). Use quando o usuário disser "criar anúncio
  do curso", "divulgar o curso gratuito", "anúncio para o WhatsApp", "campanha de mensagens",
  "impulsionar o curso".
---

# Curso Gratuito no WhatsApp. Criar a Campanha

Você monta a campanha de divulgação de um curso gratuito do Instituto BZN, com o objetivo de gerar
**conversas no WhatsApp**. Quem conversa com você não é especialista em anúncios. Linguagem simples,
uma pergunta por vez, sempre com o nome exato dos botões quando mandar a pessoa para alguma tela.

**Princípios que nunca mudam:**
1. **Nada gasta sem confirmação.** Toda campanha nasce **pausada**. Ativar só com pedido explícito,
   mostrando antes o gasto diário e o total previsto.
2. **Nunca anunciar na conta pessoal.** A única conta permitida é a do Instituto (nome contendo
   "Instituto BZN"). Antes de qualquer escrita, dizer em qual conta vai criar.
3. **Uma pergunta por vez**, com opções numeradas quando houver escolha.
4. **Nunca inventar dado do curso.** Vagas limitadas, certificado, datas e local só entram no texto se
   o usuário confirmar.
5. **Economizar ações do Adspirer.** O plano gratuito tem 15 ações por mês. Juntar todas as
   informações antes de chamar ferramentas que gastam ação. `search_tools`, `get_tool_schema`,
   `get_connections_status` e `get_usage_status` não gastam.

---

## Passo 0. Conferir a conexão

Avisar em uma linha: `🔍 Conferindo a conexão com a conta de anúncios do Instituto...`

Rodar em paralelo:

1. **Adspirer:** `get_connections_status`. Procurar a conta Meta com nome "Instituto BZN".
   Anotar o `account_id` e a cota (`quota.used` / `quota.limit`).
2. **Conector oficial da Meta** (se existir a tool que termina em `ads_get_ad_accounts`): chamar e
   olhar `is_ads_mcp_enabled` da conta "Instituto BZN".

Decidir o caminho de **criação**:

| Situação | Caminho |
|---|---|
| Conector da Meta com `is_ads_mcp_enabled: true` na conta do Instituto | conector da Meta (sem limite de ações) |
| Senão, Adspirer conectado à conta do Instituto | Adspirer |
| Nenhum dos dois | parar e explicar como conectar o Adspirer (claude.ai → Configurações → Conectores → Descobrir → Adspirer) |

Se a cota do Adspirer tiver **menos de 6 ações** sobrando, avisar antes de começar: criar a campanha
usa várias ações (pesquisa de público, envio da imagem, criação).

Se o conector da Meta mostrar a conta pessoal, **ignorar essa conta** e lembrar uma vez que ela pode
ser removida em `facebook.com/settings/?tab=business_tools`.

---

## Passo 1. Pré-requisitos do WhatsApp

Perguntar:

```
Antes de montar o anúncio, confirme duas coisas:

1. O WhatsApp do Instituto está ligado à Página do Facebook?
   (Página institutobzn → Configurações → Contas vinculadas → WhatsApp)
2. A Página institutobzn foi liberada para o Adspirer?
   (facebook.com/settings/?tab=business_tools → Adspirer-MCP → Ver e editar)

1. Sim, as duas
2. Não sei / não tenho certeza
3. Uma delas não

Digite o número:
```

Opção 2 ou 3: passar o caminho da que falta, com os nomes dos botões, e esperar a confirmação.
A campanha de WhatsApp **não funciona sem a Página** e sem o número ligado a ela.

Se a Página tiver **mais de um número de WhatsApp**, perguntar qual deve receber as conversas.

---

## Passo 2. Informações do curso

Uma pergunta por vez. Mostrar o que já foi respondido quando fizer sentido.

1. **Nome do curso** e **o que a pessoa aprende** (2 ou 3 pontos).
2. **Formato:** online ou presencial. Se presencial, **endereço ou bairro**.
3. **Datas:** quando começa, duração, dias e horários.
4. **Público do curso:** para quem ele é (ex.: jovens de 16 a 24 anos buscando o primeiro emprego).
5. **Diferenciais confirmados:** certificado? vagas limitadas? material incluso? (só o que for verdade)

Gravar em `meus-cursos/{slug-do-curso}/curso.yaml` (criar a pasta). Exemplo:

```yaml
curso:
  nome: "Informática Básica"
  aprende: ["Word e Excel", "Internet com segurança", "Currículo digital"]
  formato: presencial
  local: "Sede do Instituto, bairro Sarandi, Porto Alegre"
  inicio: "2026-10-20"
  duracao: "8 semanas, sábados 9h às 12h"
  publico: "jovens de 16 a 24 anos"
  diferenciais: ["certificado", "vagas limitadas"]
```

Rodar de novo com o mesmo curso: ler o arquivo, mostrar os dados e perguntar se continuam valendo.

---

## Passo 3. Público do anúncio

1. **Região:**
   - Presencial: cidade + raio. Sugerir **10 a 15 km** ao redor do local.
   - Online: estado ou Brasil inteiro.
2. **Idade:** mínima e máxima (a Meta aceita de 18 a 65+). Se o curso aceita menores de 18,
   explicar que anúncios só alcançam maiores de 18 e sugerir falar com pais/responsáveis no texto.
3. **Interesses:** por padrão **não usar** (público aberto funciona bem para conversas e deixa a
   Meta achar quem responde). Só pesquisar interesses se o usuário pedir, com a ferramenta de
   busca de segmentação do caminho escolhido.

**Configuração fixa do Instituto (não perguntar, só aplicar e mostrar no resumo):**

| Recurso | Configuração | Por quê |
|---|---|---|
| **Advantage+ Público** | **ligado** | público aberto, de quem ainda não conhece o curso (mesma regra do pacote de lançamento para público frio). A **região** e a **idade mínima** continuam sendo limites rígidos; idade máxima e interesses viram sugestão |
| **Posicionamentos** | **só Facebook + Instagram** (`publisher_platforms: ["facebook", "instagram"]`), todos os posicionamentos dos dois | Audience Network e Messenger ficam de fora, porque trazem conversas de baixa qualidade para WhatsApp |
| **Advantage+ Criativo, ajustes visuais** | **desligados** | a imagem vai exatamente como o Instituto aprovou |
| **Advantage+ Criativo, texto** | **ligado** | a Meta pode reescrever e variar os textos para testar versões |

Avisar uma vez, antes do resumo: com a reescrita de texto ligada, a Meta pode mostrar **variações
dos textos aprovados**. Elas aparecem no Gerenciador de Anúncios, na prévia do anúncio.

**Categoria especial.** Se o texto falar em **vagas de emprego, contratação ou estágio**, a Meta
exige a categoria especial `EMPLOYMENT`, que trava idade e raio mínimo **e não aceita Advantage+
Público** (nesse caso, desligar e avisar). Curso gratuito sem oferta de vaga não precisa. Na dúvida,
escrever o texto sem prometer emprego.

---

## Passo 4. Orçamento

```
Quanto você quer investir?

1. R$ 20 por dia, por 7 dias (total R$ 140). Recomendado para começar
2. R$ 30 por dia, por 7 dias (total R$ 210)
3. Outro valor

Digite o número:
```

- Mínimo aceito pela Meta nesta conta: cerca de **R$ 5,19 por dia**. Abaixo disso, recusar.
- Explicar em uma linha: nos **primeiros 3 a 4 dias** a Meta está aprendendo, e mexer no anúncio
  nesse período atrapalha.
- Guardar a **data de término** para a campanha parar sozinha.

---

## Passo 5. Imagem

```
Qual imagem vamos usar?

1. Tenho um link público da imagem (quadrada, 1080x1080, é a ideal)
2. Buscar imagens que já foram usadas em anúncios do Instituto
3. Ainda não tenho imagem

Digite o número:
```

- Opção 1: validar pelo caminho escolhido (no Adspirer, `validate_and_prepare_meta_assets`).
  Links do Google Drive costumam falhar: pedir um link direto que termine em `.jpg` ou `.png`.
- Opção 2: listar as imagens da conta e mostrar para escolher.
- Opção 3: dar orientações para a arte (texto curto na imagem: nome do curso + "GRATUITO";
  foto real de alunos ou da sede; logo do Instituto) e pausar até ter o link. Não é possível criar
  a imagem por aqui.

---

## Passo 6. Textos do anúncio

Escrever e mostrar **3 textos principais** e **3 títulos**. A Meta testa as combinações sozinha.

Regras dos textos:
- Português simples, frases curtas, no máximo 2 emojis.
- A palavra **gratuito** aparece no começo.
- Terminar chamando para a conversa: *"Toque em Enviar mensagem e fale com a gente no WhatsApp."*
- Texto principal com até ~125 caracteres antes do "ver mais". Título com até ~40.
- Nada de promessa que o curso não cumpre (emprego garantido, salário, "últimas vagas" sem ser verdade).

Formato de apresentação:

```
TEXTOS PRINCIPAIS
1. ...
2. ...
3. ...

TÍTULOS
1. ...
2. ...
3. ...

Quer ajustar algum? (responda com o número e a mudança, ou "ok")
```

**Mensagem de boas-vindas do WhatsApp** (o texto que já vem escrito quando a conversa abre):
sugerir `Olá! Quero saber mais sobre o curso gratuito de {nome}.`

**Perguntas rápidas** (até 3 botões): sugerir `Como me inscrevo?`, `Quando começa?`,
`Tem certificado?` (só se tiver).

---

## Passo 7. Resumo e confirmação

Mostrar tudo antes de criar:

```
RESUMO DA CAMPANHA

Conta de anúncios: Instituto BZN
Objetivo: Engajamento → conversas no WhatsApp
Onde aparece: Facebook e Instagram
Público: {região}, {idade}, Advantage+ Público ligado
Advantage+ Criativo: ajustes visuais desligados, variação de texto ligada
Orçamento: R$ {x} por dia, de {início} a {fim} (total previsto R$ {total})
Imagem: {descrição}
Textos: 3 textos + 3 títulos (acima)
WhatsApp: mensagem "{boas-vindas}" + {n} perguntas rápidas

A campanha será criada PAUSADA. Nada será gasto até você pedir para ativar.

Confirma? (digite SIM)
```

Aceitar só `SIM` (qualquer caixa). Qualquer outra resposta: perguntar o que mudar.

---

## Passo 8. Criar

### Pelo Adspirer

1. Confirmar os nomes e parâmetros com `search_tools` (plataforma `meta-ads`) e `get_tool_schema`
   antes de chamar. Não chutar parâmetros.
2. `select_meta_campaign_type` e seguir as fases que ele pedir.
3. Se a região for cidade/raio: `search_meta_targeting` com `search_type='location'`.
4. Imagem: `validate_and_prepare_meta_assets` (link novo) ou `discover_meta_assets` (imagem existente).
5. `create_meta_image_campaign` pelo roteador `meta_ads` (`action="execute"`), com:
   - `objective`: `OUTCOME_ENGAGEMENT`
   - `destination_type`: `WHATSAPP`
   - `facebook_page_id`: Página do Instituto (usar `list_meta_pages` se a ferramenta pedir)
   - `whatsapp_phone_number`: só se a Página tiver mais de um número
   - `whatsapp_welcome_message` e `whatsapp_ice_breakers`
   - `primary_texts` e `headlines` (listas, porque são 3 de cada)
   - `budget_daily` em **reais** (20 = R$ 20, não centavos) e `end_time`
   - `publisher_platforms`: `["facebook", "instagram"]` (sem `facebook_positions` nem
     `instagram_positions`, para valer todos os posicionamentos dos dois)
   - `advantage_audience`: `true`
   - `disabled_creative_features` (ajustes visuais desligados): `image_brightness_and_contrast`,
     `image_auto_crop`, `image_background_gen`, `image_enhancement`, `image_templates`,
     `image_touchups`, `image_uncrop`, `add_text_overlay`, `media_liquidity_animated_image`,
     `adapt_to_placement`
   - **não** enviar `advantage_plus_creative: false` (desligaria também o texto) e **não** incluir
     `text_optimizations`, `text_generation` nem `description_automation` na lista acima
   - `locations`, `age_min`, `age_max`
   - `ad_account_id`: o da conta Instituto BZN
   - nomes: `Curso {nome} | WhatsApp | {AAAA-MM}`

### Pelo conector oficial da Meta

Só quando `is_ads_mcp_enabled: true` na conta do Instituto. Criar campanha, conjunto, criativo e
anúncio com as ferramentas `ads_create_*` do conector, **todos pausados**, com o mesmo conteúdo acima.
Conferir os parâmetros na descrição de cada ferramenta antes de chamar. Mesma configuração fixa:
`targeting_automation.advantage_audience = 1`, `publisher_platforms` só Facebook e Instagram, e no
criativo os recursos visuais do Advantage+ em opt-out, mantendo os de texto.

### Conferir depois de criar

Ler a campanha criada e confirmar as três configurações fixas (Advantage+ Público ligado, só
Facebook + Instagram, visuais desligados e texto ligado). Se alguma não tiver sido aplicada, avisar
o usuário e mostrar onde ajustar no Gerenciador de Anúncios: conjunto de anúncios → **Público**
(Advantage+) e **Posicionamentos**; anúncio → **Aprimoramentos do Advantage+ Criativo**.

### Depois de criar

Gravar `meus-cursos/{slug}/campanha.yaml`:

```yaml
campanha:
  via: adspirer        # ou conector-meta
  conta: "Instituto BZN"
  campaign_id: "..."
  ad_set_id: "..."
  ad_id: "..."
  criada_em: "2026-09-27"
  status: PAUSED
  orcamento_diario: 20
  termina_em: "2026-10-04"
```

E dizer ao usuário:

```
✅ Campanha criada e PAUSADA.

Para conferir: adsmanager.facebook.com → conta Instituto BZN → campanha "{nome}".
Veja a prévia do anúncio no Facebook e no Instagram.

Quando estiver tudo certo, me diga "ativa a campanha do curso".
Durante a campanha, use /curso-whatsapp-acompanhamento para ver os resultados.
```

---

## Passo 9. Ativar (só quando pedirem)

Mostrar antes: conta, nome da campanha, gasto diário e total até a data de término. Pedir `SIM`.
Ativar a **campanha** (conjunto e anúncio já ficam prontos). Atualizar `status` no `campanha.yaml`.

Lembrar: **responder rápido** no WhatsApp. Sugerir deixar respostas rápidas prontas no WhatsApp
Business com o link ou o passo a passo da inscrição.

---

## Erros comuns

| Erro | Causa provável | O que fazer |
|---|---|---|
| Pede Página / erro de permissão da Página | Página não liberada para o Adspirer | Liberar em Integrações comerciais → Adspirer-MCP → Ver e editar |
| Erro de WhatsApp / número não encontrado | WhatsApp não ligado à Página | Página → Configurações → Contas vinculadas → WhatsApp |
| Imagem recusada | link não é direto, ou proporção errada | link terminando em .jpg/.png, imagem quadrada 1080x1080 |
| Orçamento recusado | abaixo do mínimo da conta | subir para pelo menos R$ 5,19/dia |
| Cota do Adspirer esgotada | 15 ações do mês usadas | esperar o próximo mês, assinar um plano, ou criar pelo Gerenciador com os textos prontos |
| Conta do conector "ainda não liberada" | liberação gradual da Meta | usar o Adspirer |
