# 🕸️ Scraper

Este projeto automatiza a coleta de dados de produtos, extraindo informações completas como categoria, nome, descrição, preço e abreviação de todas as categorias disponíveis, organizando tudo em uma planilha Excel.

## 🚀 Funcionalidades

- Seleciona automaticamente todas as categorias do site.
- Para cada produto:
  - Extrai **nome**, **descrição limpa**, **preço** e **abreviação**.
- Gera uma planilha Excel já formatada:
  - Coluna A: Categoria
  - Coluna B: Nome do item
  - Coluna C: Descrição (sem preço e abreviação)
  - Coluna D: Preço (pronto para análise no Excel)
  - Coluna E: Abreviação

## 💻 Pré-requisitos

- Python 3.7+
- Google Chrome instalado
- ChromeDriver compatível com sua versão do Chrome ([Download aqui](https://sites.google.com/chromium.org/driver/))
- Pacotes Python:
  - `selenium`
  - `pandas`
  - `openpyxl` (para exportar Excel)

Instale as dependências com:

```bash
pip install selenium pandas openpyxl
