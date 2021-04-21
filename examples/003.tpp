
preeenche_vetor(inteiro: vetor[], inteiro: tamanho) 
  inteiro: indice
  indice := 0

  repita
    se indice > 2 então
      vetor[indice] := -indice
    senão
      vetor[indice] := indice
    fim
    indice += 1
  até indice >= tamanho
fim

flutuante processa_vetor(inteiro: vetor[], inteiro: tamanho) 
  inteiro: indice
  inteiro: resultado
  indice := 0 
  resultado := 0 

  repita
    se vetor[indice] > 0 então
      resultado += vetor[indice]
    senão
      resultado -= 1
    fim
    indice += 1
  até indice >= tamanho

  retorna(resultado)
fim
{UM comentário qualquer\}{asdfadfadfas\}}

inteiro principal() 
  inteiro: tamanho
  inteiro: vetor[5]
  tamanho := 5

  preeenche_vetor(vetor, tamanho)

  flutuante: resultado 
  resultado := processa_vetor(vetor, tamanho)

  escreva(resultado)

  retorna(0)
fim
