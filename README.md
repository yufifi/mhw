# MHW Web Scraping Database

--- 

## Introdução
Este repositório foi criado para extrair os dados do site https://mhworld.kiranico.com/pt-BR/monsters e exportar esses dados para um arquivo chamado monsters.csv.

--- 

## Utilização
Para utilizar o projeto é inicializar o venv da seguinte forma dentro do diretório mhw/:

```bash
source .venv/bin/activate
```
Depois basta utilizar o comando a seguir:

```bash
scrapy crawl monster_spider
```

---

## DEPENDÊNCIAS
> [!IMPORTANT]
> **As dependências que foram utilizadas no projeto são:**
> - Scrapy
> - Python 3.12.6
