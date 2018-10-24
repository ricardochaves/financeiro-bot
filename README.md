# Bot Financeiro

## Eu fiz isso porque

A muitos anos eu faço meu controle financeiro, para tal, eu utilizei e busquei muitas ferramentas para me ajudar, antes mesmo de existir os smartfones, quem aí já usou o [Microsoft Money](https://pt.wikipedia.org/wiki/Microsoft_Money)?, então, eu já.
O problema com todas as soluções que eu vi é que elas têm que se tornar o mais genérica possível para poder atingir o máximo de pessoas, isso acaba tornando elas difíceis de usar ou no melhor cenário, pedir muitas informações para fazer um lançamento.

No meu caso, como eu acredito que é o mesmo que a maioria de pessoas que tenta um controle pessoal, não tenho tempo para cadastrar cada transferência bancária, recarga de cartão de transporte, etc.

A solução para meu problema foi reduzir o máximo possível de informações que eu vou controlar. Cheguei ao mínimo necessário para conseguir tirar os relatórios que eu preciso, por exemplo, eu não me importo em onde está o dinheiro, cartão de alimentação, cartão de transporte e conta bancária são a mesma coisa, afinal, tudo é dinheiro.

## Objetivo

- Ao cadastrar o que se gasta você passar a ser mais responsável para gastar
- Saber o que é custo fixo e o que é variável, variável é o que você pode parar de gastar para economizar.
- Saber onde você gasta mais.

Com os itens acima você vai conseguir três coisas muito importantes:

Primeiro que cadastrando cada gasto e ganho de dinheiro você passa a questionar se o gasto é realmente necessário e se alegra com cada entrada de dinheiro, mesmo sendo apenas um real de lucro com investimento da sua poupança.

Segundo, vai poder estipular metas para não gastar mais de X reais no mês e para controlar esse gasto no seu dia a dia você pode filtrar todos os custos variáveis e pode combater o excesso de gastos onde realmente pode ser combatido.

Terceiro, ao saber onde você mais gasta dinheiro é possível questiona a médio prazo as decisões que você tem tomado, exemplo: vale a pena pagar esse aluguel mesmo? Eu não vou na varanda a um mês, será que seria possível economizar três mil reais em um ano morando em um lugar sem a varanda? Será que eu preciso desse plano pós pago de telefone? E essa internet de quatro milhões de megas?

## Banco de dados

A ideia é ter uma grande tabela com todos os dados e a partir dela extrair os dados, simples assim. Para isso funcionar nós, temos:

`Records` onde todos os movimentos financeiros são cadastrados, alguns campos são tabelados para organizar os relatórios, esses campos são: `TypeEntry` (Fixo e Variável), `FamilyMember` (Membos da sua família, Ricardo, Isabele, etc), `Category` (Casa, Carro, Trabalho, etc).

## Planilha Google

Data Lanc - Data Fatura - Débito - Crédito - Total - Categoria - Nome - Descrição - Tipo de custo

Sendo que Total é uma coluna de formula que o bot deixa em branco.
Isso é feito via API do Google e pelo pacote [google-api-python-client](https://github.com/googleapis/google-api-python-client)

## Comandos para o bot

Em `FullCommand` você pode cadastrar comandos para usar no bot. Vou detalhar como funciona cada campo:

- **Comando**: É exatamente o que você precisa digitar no bot, basicamente o bot faz uma query no que você digitou e nesse campo, se achar, ele executa.

- **Data de Lançamento**: Usa data do dia?: Se marcado ele vai colocar a data de lançamento com a data atual, se não marcar ele vai te perguntar a data.

- **Data de Pagamento**: É a data de pagamento daquele lançamento, quando realmente o dinheiro sai da sua conta, as opções são:
- - **Data do dia**: Vai utilizar a data atual
- - **Data do Cartão** (15): Se a data atual for dia 8 ou maior ele vai lançar a saída para o dia 15 do mês seguinte, se menor que dia 8 vai usar o dia 15 do mês atual. (Criar issues para melhorar isso)
    Perguntar: Vai te perguntar qual data usar.

- - **Dia Seguinte**, **Mês Seguinte**, **Dia 5 mês vigente**, **Dia 5 mês que vem** já são auto explicativos.

- **Débito**: É o valor de débito que ele vai usar, vazio e ele vai te perguntar o valor.
- **Crédito**: É o valor de crédito que ele vai usar, vazio e ele vai te perguntar o valor.

**Categoria**, **Nome**, **Descrição** e **Tipo** são os valores padrões usados, se não informados, ele vai perguntar

Existem limitações na data de cartão de crédito sobre a data do dia bom e do dia de pagamento. Ideias para resolver essas datas.

## Agendamentos

O projeto tem um sistema de agendamentos para o bot lembrar de alguns lançamentos, para isso eu implementei um [Django Q](https://django-q.readthedocs.io/en/latest/) e dentro do arquivo `schedule.py` existe um metodos para ser executado recebendo uma `string` com o seguinte formato:

```json
{
  "verify": {
    "query": { "debit": 12, "name": 1 },
    "when": "day"
  },
  "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
  "message": {
    "user": "769652847",
    "text": "Você ainda não lançou o almoço de hoje! /ar12 /ar19 ou /arv"
  }
}
```

A estruta acima funciona da seguinte forma:

Se existir a chave `verify` ele vai executar a query da key na tabela de `Records`, caso ele encontre alguma coisa ele não vai fazer mais nada. A ideia é você poder cadastrar coisas como: Todo dia às 13h ele vai verificar se você já lançou o seu almoço, caso ele não ache o almoço ele vai passar dessa parte, também pode verificar se esse mês você já cadastrou a conta de luz.

A key `message` define o que e para quem ele vai enviar a notificação. O `user` é o usuário do Telegram para quem o bot vai enviar a mensagem que está em `text`.

## Relatórios

Bom, tudo isso é inútil se a gente não tiver relatórios, certo?

No próprio administrativo você já tem um filtros para conversar ver algumas coisas básicas. Além disso eu estou montando um aplicativo que faz acesso via API ao nosso sistema e entrega alguns relatório básicos. Esse aplicativo está [nesse repositório](https://github.com/ricardochaves/FinanceiroApp).

## Sentry

O projeto loga os erros no [Sentry](https://sentry.io/) e para isso você vai precisar configurar um projeto seu. No site deles você acham mais detalhes.

## .env File

Você vai pecisar de um arquivo `.env` com as seguinte variáveis:

```
GUNICORN_WORKS=1
PORT=5005
DEBUG=True

DB_DATA_BASE=base_site
DB_USER=root
DB_PASSWORD=example
DB_HOST=db
DB_PORT=3306

SERVICE_ACCOUNT_FILE=bot-financeiro-1534199345603-f2129fd5303c.json

TELEGRAN_TOKEN=695792236:ABBFhwwaILseFKKb7nj1QqFYhtmGB8h07WM

SENTRY_DNS=https://b657f6061c34533ecas4n6n64kf9832cde@sentry.io/1375930
```

As três últimas variáveis eu coloquei valore bem perto dos reais para facilitar entender.
