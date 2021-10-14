# Ferrovia STR

Projeto da disciplina Sistemas de Tempo Real.

## Descrição do problema

Implementar um programa que simula a dinâmica de 3 trens (verde, roxo e vermelho) se locomovendo independentemente em 3 circuitos que possuem trilhos compartilhados.

### Restrições

- Os trilhos compartilhados (L3, L4 e L6) só permitem a passagem de um trem por vez;
- Não podem haver deadlocks, isto é, os trens não podem ficar travados, sem possibilidade de movimento;

### Requisitos

- Interface gráfica mostrando o movimentos dos trens em seus circuitos;
- Controles para modificar a velocidade dos trens;

## Como executar

- Clonar repositório e executar arquivo app.py da seguinte forma:

```
$ python app.py
```

## Notas do desenvolvimento

- Como sugerido no enunciado da atividade, criar 5 threads com as seguintes finalidades:

  - 1 pra movimentar cada trem
  - 1 pra controlar a velocidade dos trens
  - 1 pra exibir os trens

- Nos trilhos compartilhados, existe uma região crítica que deve ser acessada por apenas um trem de cada vez. Então, precisam ser usados artifícios para o controle do acesso a essas regiões, como por exemplo os mutex, que limitam a utilização de um determinado trecho de código para apenas uma thread por vez.

- Para evitar deadlocks, os trechos compartilhados (recursos) devem ser alocados completamente para um determinado trem e só depois que forem liberados é que podem ser alocados novamente para outro trem.
