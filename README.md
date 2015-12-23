# TP Processamento de Dados Massivos
Trabalho Prático Final da disciplina de Processamento de Dados Massivos 2015/2

## Crawler

### Instalando

Recomenda-se o uso de virtualenvs para instalar o Scrapy.

Com o virtualenv executando, instale as dependencias com

`pip install -r requirements.txt`

### Executando o crawler

Para iniciar ou continuar o crawler com pausa habilitada, execute:

`scrapy crawl meetup -s JOBDIR=crawls/somespider-1 -o groups.json`

Para parar o crawler, basta apertar ctrl+c 1 vez e aguardar as requests pendentes serem salvas (apertar 2 vezes faz com q o arquivo final fique corrompido)

O arquivo com os dados de saida eh `groups.json`

## GraphX

Com o spark instalado e o SBT (Simple Building Tool), baixe todas as dependencias e compile o codigo com:

`sbt package`

Em seguida, execute o código com o comando:

`/caminho/para/spark/bin/spark-submit --class "MeetupAnalysis" --master local[4] target/scala-2.10/meetup-analysis-project_2.10-1.0.jar pagerank caminho/para/arquivo/entrada/data/edges50.txt --numEPart=1`