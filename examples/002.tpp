
principal()
    inteiro: x
    x := 10
    x += x++

    repita
        se x > 0 então
            x += 1
        senão
            x -= 1
        fim
    até ((x > 0 && x < 100) || (x < 0 && x > -100))

    retorna (0)
fim
