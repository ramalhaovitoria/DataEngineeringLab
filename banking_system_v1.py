menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
deposito = 0
saque = 0
extrato = ""
LIMITE_SAQUE = 500

while True:
    opcao = input(menu)
    if opcao == "q":
        break
    elif opcao == "d":
        deposito = float(input("Digite o valor do depósito: "))
        saldo += deposito
        extrato += f"Depósito de R$ {deposito:.2f}\n"
    elif opcao == "s":
        saque = float(input("Digite o valor do saque: "))
        if saque > saldo:
            print("Saldo insuficiente")
        elif saque > LIMITE_SAQUE:
            print("Limite de saque diário excedido")
        else:
            saldo -= saque
            extrato += f"Saque de R$ {saque:.2f}\n"
    elif opcao == "e":
        print(f"Saldo: R$ {saldo:.2f}")
        print("Extrato:")
        print(extrato)
    else:
        print("Opção inválida")