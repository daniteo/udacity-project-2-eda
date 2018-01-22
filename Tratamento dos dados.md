# Tratamento de dados

Antes de uma analise dos dados foi necessário o tratamento do dataset. Foram identificdas as seguintes necessidades de tratamento:

 - *contb_receipt_amt* (valor da contribuição)
 - *contb_receipt_dt* (data da contribuição)
 - *contbr_city* (cidade do contribuinte)
 - Inclusão de novos campos
   - partido dos candidatos
   - nome dos comites

## Campo contb_receipt_amt - Valor da contribuição 

É possível verificar que algus dos valores de contribuições inferiores a 0. Como não existem contirbuições com valor negativo, para estes registros podem ser feitos 2 tipos de tratamentos: considerar o valor absoluto ou eliminá-los do dataset. Irei considerar que todos os valores deveriam ser positivos e remover do conjunto de dados os registro com contibução igual a 0.

## Campo contb_receipt_dt - Data da contribuição

As datas estão da base de dados estão armazenadas como texto no formato DD-MMM-AA. Separei os componentes da data em colunas para dia, mês e ano. 

## Campo election_tp - Tipo de eleição

Para o tipo de eleição foi considerado o seguinte tratamento:

- Para os tipos vazios, foi considerada a data da contribuição. Contribuições ocorridas a partir de abril/2016 foram consideradas como "G2016" e aquelas anteriores a esta data foram consideradas "P2016".
- As ocorrencias com o tipo "P2012" foram alterados para "P2016"

## Campo contbr_city - Cidade do contribuinte

No resumo percebi que o número de cidades diferentes dos contribuintes era muito grande (2327 cidades). Numa analise dos dados notei que mesmas cidades estavam registradas com grafia diferentes, por erro ou abreviação do nome. Um exemplo seria o Brooklyn que aparece na base de dados com diversos nomes: BROOKLIN, BROOKLN, BROOKLY, BROOKLYB e BROOKLYN, entre outros.

Para o tratamento destas cidades existem duas soluções possíveis:

 - Um mapeamento dos diversos nomes da mesma cidade para um único nome comum
 - Uso de uma base de dados de cidades e mapea-las com base nos ceps (zipcode) dos contribuintes. Optei por esta segunda opção.
 
Neste caso realizei um `left join` da base de dados de financiamento de campanhas com o dataset `zipcode`. Este data set contem CEPs das cidades americanas, com o nome da cidade, estado, longitude e latitude de cada localização. Para este mapeamento foi considerado apenas os 5 primeiros digitos do cep do contribuinte para relação com o dataset `zipcode`.
 
Após mapearmos os CEPs, ainda restanram 617 registros para os quais não foram identificados o CEP. Para este registros o valor médio de contribuição é de U$ 178,80. E um total de U$ 110.290,2, equivalente a 0.06% da contribuição total. Com base nestas informações, optei por fazer a exclusão destes registros da base de dados de financiamento de campanha.

## inclusão de novas colunas

Para a inclusão das novas informações, utilizei duas bases de dados obtidas do site do [FEC - Federal Election Comission](http://classic.fec.gov/finance/disclosure/ftpdet.shtml):
    - Candidatos 
    - Comites

### Partidos

Para os partidos cruzei as informações da coluna `cand_id` (id do candidato), e acrescentei a coluna `party`, com o partido a qual pertence o candidato

### Nome do comite

A partir da base de dados, identifiquei o nome do comite com base na coluna `cmte_id` e adicionei uma nova coluna com o nome `cmte_nm`