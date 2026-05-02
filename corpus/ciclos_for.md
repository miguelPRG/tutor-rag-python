# Ciclos For

O ciclo `for` é usado para repetir um bloco de código um determinado número de vezes ou para percorrer uma lista.

## Usar com range():
A função `range(n)` cria uma sequência de 0 até n-1.
```python
for i in range(5):
    print(i) # imprime 0, 1, 2, 3, 4
```

## Percorrer Listas:
```python
frutas = ["maçã", "banana", "laranja"]
for fruta in frutas:
    print(fruta)
```

## Erro Comum:
Tentar modificar a lista enquanto a percorres com um `for` simples pode causar comportamentos inesperados.

## Pergunta Orientadora:
Se tivesses uma lista de compras, como poderias imprimir cada item precedido por um número?
