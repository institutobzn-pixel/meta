# Claude na Página do Facebook e no Instagram

Robô que responde automaticamente, usando o Claude, as mensagens enviadas para a
**Página do Facebook (Messenger)** e para o **Direct do Instagram**.

```
Pessoa manda mensagem ──► Meta ──► este servidor ──► Claude
                                         │
Pessoa recebe a resposta ◄── Meta ◄──────┘
```

Você vai precisar de **4 chaves**. Anote cada uma num bloco de notas conforme for
pegando:

| Chave | O que é | Onde pegar |
|---|---|---|
| `ANTHROPIC_API_KEY` | chave do Claude | Parte 1 |
| `PAGE_ACCESS_TOKEN` | token da Página | Parte 3 |
| `META_APP_SECRET` | senha secreta do app | Parte 2 |
| `META_VERIFY_TOKEN` | uma senha que **você inventa** (ex.: `instituto2026`) | — |

---

## Parte 0 – Antes de começar (confira)

- [ ] Você é **administrador** da Página do Facebook.
- [ ] O Instagram é uma conta **Profissional** (Empresa ou Criador de conteúdo).
- [ ] O Instagram está **ligado à Página do Facebook**. Para conferir, no Facebook abra
      a Página → **Configurações → Contas vinculadas → Instagram**.
- [ ] No app do Instagram, vá em **Configurações → Mensagens e respostas aos stories →
      Ferramentas conectadas** e **ative "Permitir acesso às mensagens"**.

## Parte 1 – Chave do Claude

1. Acesse **console.anthropic.com** e crie uma conta.
2. Em **Billing**, adicione créditos (alguns dólares bastam para testar).
3. Em **API Keys**, clique em **Create Key** e copie a chave (`sk-ant-...`).
   Essa é a `ANTHROPIC_API_KEY`.

## Parte 2 – Criar o app na Meta

1. Acesse **developers.facebook.com** e entre com a mesma conta que administra a Página.
2. Clique em **Meus apps → Criar app**.
3. No caso de uso, escolha **"Interagir com clientes no Messenger da Meta"**
   (ou "Outro" → tipo **Empresa**). Dê um nome e crie.
4. No menu da esquerda, abra **Configurações do app → Básico**. Em **Chave secreta do
   aplicativo**, clique em **Mostrar** e copie. Essa é a `META_APP_SECRET`.

## Parte 3 – Pegar o token da Página

1. No painel do app, abra **Messenger → Configurações da API do Messenger**.
   Se não aparecer, clique em **Adicionar produto** e adicione **Messenger**.
2. Em **Gerar tokens de acesso**, clique em **Conectar** e escolha a sua Página.
   Marque também o Instagram, se ele aparecer.
3. Clique em **Gerar** ao lado da Página e copie o token (`EAA...`).
   Esse é o `PAGE_ACCESS_TOKEN`.

> O mesmo token serve para o Facebook **e** para o Instagram, porque o Instagram está
> ligado à Página.

## Parte 4 – Colocar o servidor no ar (Render, gratuito)

1. Acesse **render.com** e entre com a sua conta do **GitHub**.
2. Clique em **New → Blueprint** e escolha este repositório (`meta`).
   O Render lê o arquivo `render.yaml` e configura tudo sozinho.
3. Ele vai pedir as 4 chaves. Cole cada uma no campo com o mesmo nome.
4. Clique em **Apply / Deploy** e espere terminar (alguns minutos).
5. Copie o endereço que aparece no topo, algo como `https://meta-claude-xxxx.onrender.com`.
   Abra esse endereço no navegador: se aparecer **ok**, o servidor está no ar. ✅

## Parte 5 – Ligar a Meta ao servidor (webhook)

### Facebook (Messenger)
1. Volte em **Messenger → Configurações da API do Messenger**.
2. Em **Configurar webhooks**, preencha:
   - **URL de retorno de chamada**: o seu endereço + `/webhook`
     (ex.: `https://meta-claude-xxxx.onrender.com/webhook`)
   - **Token de verificação**: a senha que você inventou (`META_VERIFY_TOKEN`)
3. Clique em **Verificar e salvar**.
4. Na lista de Páginas (seção dos tokens), clique em **Adicionar assinaturas** ao lado da
   sua Página e marque **`messages`**. Salve.

### Instagram
1. No menu, abra **Messenger → Configurações do Instagram**
   (em alguns painéis aparece como **"API do Messenger para Instagram"**).
2. Em **Webhooks**, use **a mesma URL e a mesma senha** do passo anterior.
3. Assine o campo **`messages`**.

## Parte 6 – Testar

1. Com **outra conta** (não a da Página), mande uma mensagem para a Página no Messenger.
2. Mande também uma mensagem no Direct do Instagram.
3. A resposta do Claude deve chegar em alguns segundos. 🎉

> **Importante: modo de teste.** Enquanto o app estiver em modo de desenvolvimento,
> **só pessoas com função no app** (administradores, desenvolvedores e testadores)
> recebem resposta. Para adicionar alguém, use **Funções do app → Funções**.
> Para liberar o robô para **todo mundo**, veja a Parte 7.

## Parte 7 – Liberar para o público (quando estiver tudo funcionando)

1. Em **Configurações do app → Básico**, preencha a **URL da Política de Privacidade**
   e o ícone do app.
2. Em **Revisão do app → Permissões e recursos**, peça **acesso avançado** para:
   `pages_messaging`, `instagram_manage_messages`, `instagram_basic`,
   `pages_manage_metadata`.
3. A Meta pede um vídeo curto mostrando o robô respondendo. A análise leva alguns dias.
4. Quando aprovar, mude o app para o modo **Ao vivo**.

---

## Personalizar o jeito que o Claude responde

No Render, abra **Environment** e crie a variável `SYSTEM_PROMPT` com as instruções.
Por exemplo:

```
Você é o assistente do Instituto BZN. Responda em português, de forma simpática e curta.
Nosso horário é de segunda a sexta, das 8h às 18h. Endereço: ...
Para matrículas, direcione para o site ...
Se não souber a resposta, diga que a equipe vai responder em breve.
```

Quanto mais informações sobre o Instituto você colocar aí, melhores serão as respostas.

## Problemas comuns

| Sintoma | O que fazer |
|---|---|
| "Não foi possível validar a URL" ao salvar o webhook | Confira se a URL termina em `/webhook` e se a senha é **exatamente** igual à `META_VERIFY_TOKEN` no Render. |
| O servidor demora a responder na primeira mensagem | O plano gratuito do Render "dorme" depois de 15 min parado e leva ~1 min para acordar. Para uso real, use um plano pago. |
| Nenhuma resposta chega | No Render, abra **Logs** e procure mensagens como `Erro da Meta` ou `Erro ao responder`. |
| Funciona para você, mas não para outras pessoas | O app está em modo de teste (veja a Parte 6 e a Parte 7). |
| Instagram não responde, mas o Facebook sim | Confira a Parte 0 (conta profissional, ligada à Página, "Permitir acesso às mensagens") e a assinatura `messages` do Instagram. |
| `Erro da Meta (190)` nos logs | O token da Página expirou ou está errado. Gere outro (Parte 3) e atualize no Render. |

## Detalhes técnicos

- Código: `app.py` (Python + Flask). Modelo padrão: `claude-opus-5`; dá para trocar pela
  variável `CLAUDE_MODEL`, por exemplo para `claude-sonnet-5`, que é mais barato.
- Se o Claude recusar uma mensagem por segurança, a API tenta outro modelo
  automaticamente (`fallbacks: "default"`).
- O histórico da conversa (últimas 20 mensagens por pessoa) fica na memória e
  some quando o servidor reinicia.
- Mensagens longas são divididas em pedaços de até 1000 caracteres (limite do Instagram).
- Fotos, áudios e figurinhas são ignorados; só textos são respondidos.

Para rodar no seu computador:

```bash
pip install -r requirements.txt
cp .env.example .env   # preencha as chaves
export $(cat .env | xargs) && python app.py
```
