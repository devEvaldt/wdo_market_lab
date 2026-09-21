# WDO Market Lab

Projeto de apoio à decisão para operações com mini dólar WDO.

Atualmente, o exemplo lê candles de um CSV, normaliza os tipos,
ordena por timestamp, valida preços e volume, grava um Parquet
e consulta um resumo com DuckDB.

## Referência inicial

- Branch inspecionada: `feat/milestone-part2`.
- Commit de referência: `cfc4c66` — `feat: test`.
- Ambiente identificado: Python 3.13.15 e uv 0.12.3.
- Cinco testes existentes: normalização, candle válido,
  máxima inválida, volume negativo e gravação/releitura de Parquet.
- O comando `wdo-market-lab` ainda imprime apenas uma saudação.

O histórico existente mostra uma feature integrada em `develop`
pelo PR #1 e um commit posterior de testes na branch atual.

## Ambiente

Execute os comandos a partir da raiz do repositório.

Pré-requisitos: uv e Python 3.13.
O projeto declara compatibilidade com Python >=3.13.

Para preparar um novo ambiente a partir do lock existente:

```bash
uv sync --locked
```

Esse comando instala/sincroniza as dependências no ambiente do projeto.
Os comandos seguintes usam `--no-sync` para executar no ambiente
já preparado.

## Fixture

Arquivo: `tests/fixtures/sample_wdo_1m.csv`.

Os dois candles são sintéticos e não representam cotações reais.
Eles estão em ordem cronológica inversa para exercitar a ordenação.

- `timestamp`: formato `YYYY-MM-DD HH:MM:SS`, sem informação de fuso.
- `open`, `high`, `low`, `close`: preços fictícios com ponto decimal.
- `volume`: quantidade inteira fictícia, sem unidade de mercado definida.
- A interpretação do fuso e da unidade de volume dos dados reais
  ainda precisa ser definida.

## Testes

```bash
uv run --no-sync pytest -v
```

Resultado esperado: cinco testes aprovados.

Os testes criam seus próprios dados; eles não dependem do CSV
do exemplo. O teste de Parquet utiliza uma pasta temporária.

## Reprodução do exemplo

Copie a fixture para o caminho esperado pelo processamento:

```bash
mkdir -p data/raw/wdo
cp tests/fixtures/sample_wdo_1m.csv data/raw/wdo/sample_wdo_1m.csv
```

Execute a normalização e a consulta:

```bash
uv run --no-sync python -m wdo_market_lab.market_data.normalization.normalize_wdo
uv run --no-sync python scripts/query_wdo.py
```

A normalização gera `data/processed/wdo/sample_wdo_1m.parquet`.
Reexecutá-la sobrescreve esse arquivo de saída.

O resultado deve conter dois candles em ordem crescente de timestamp.
A consulta deve apresentar:

| Campo | Valor esperado |
|---|---|
| candles | 2 |
| first_candle | 2026-08-20 10:00:00 |
| last_candle | 2026-08-20 10:01:00 |
| minimum_price | 5399.5 |
| maximum_price | 5405.0 |
| total_volume | 2730 |

A fixture deve acompanhar o código no Git. As cópias em `data/`
e o Parquet gerado permanecem ignorados.

## Dados ainda necessários

- Fonte e forma de obtenção dos dados reais.
- Amostra real e descrição das suas colunas.
- Contrato/vencimento do WDO e período disponível.
- Fuso horário e significado do timestamp de cada candle.
- Unidade e significado do volume.

## Checklist do Milestone 0

- [ ] Ambiente preparado e identificado.
- [ ] Cinco testes executados e aprovados.
- [ ] Fixture documentada disponível no repositório.
- [ ] Parquet gerado a partir da fixture.
- [ ] Ordenação e resumo conferidos com os valores esperados.
- [ ] README e fixture incluídos no controle de versão.
- [ ] Pendências dos dados reais registradas.