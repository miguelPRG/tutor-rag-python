# Condicionais: if, elif, else

As condicionais permitem que o teu programa tome decisões. O código só é executado se uma condição for verdadeira.

## Estrutura Básica:
```python
if condicao:
    # código executado se verdadeiro
elif outra_condicao:
    # código se a primeira for falsa e esta verdadeira
else:
    # código se nenhuma anterior for verdadeira
```

## Importância da Indentação:
Em Python, o espaço à esquerda (normalmente 4 espaços) define o que está "dentro" do bloco `if`.

## Exemplo:
```python
nota = 15
if nota >= 10:
    print("Aprovado")
else:
    print("Reprovado")
```

## Erro Comum:
Esquecer os dois pontos (`:`) no final da linha do `if`.

## Pergunta Orientadora:
Como verificarias se um número guardado numa variável é par ou ímpar?
