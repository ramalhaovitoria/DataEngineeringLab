import textwrap

def menu ():
    return input(textwrap.dedent("""
    1 - Sacar
    2 - Depositar
    3 - Extrato
    4 - Criar usuário
    5 - Criar conta
    6 - Listar contas
    7 - Sair
    """))

def depositar(saldo, valor, extrato, /):
    if valor <= 0:
        return "Valor de depósito deve ser positivo."
    else:
        saldo += valor
        extrato += f"Depósito: R${valor:.2f}"
        return f"Depósito de R${valor:.2f} realizado com sucesso."
    
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_por_valor = valor > limite
    excedeu_por_saques = numero_saques >= limite_saques
    excedeu_por_saldo = valor > saldo
    
    if excedeu_por_saques:
        print("Limite diário de saques atingido.")
    
    elif excedeu_por_valor:
        print("Valor de saque excede o limite permitido de 500 por vez.")
    
    elif excedeu_por_saldo:
        print("Saldo insuficiente.")
    
    elif valor > 0:
        saldo -= valor
        numero_saques += 1
        extrato += f"Saque: R${valor:.2f}"
        return f"Saque de R${valor:.2f} realizado com sucesso. Saques restantes: {limite_saques - numero_saques}."
    
    else:
        return "Valor de saque deve ser positivo."
    
    return saldo, extrato
    
def exibir_extrato(saldo,/,*, extrato):
    if not extrato:
        return "Sem transações realizadas."
    else:
        return "\n".join(extrato)

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("CPF já cadastrado.")
        return
    
    nome = input("Digite o nome completo do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário (dd-mm-aaaa): ")
    email = input("Digite o email do usuário (nome@exemplo.com): ")
    endereco = input("Digite o endereço do usuário (logradouro, numero, bairro - Cidade/Estado - CEP): ")

    usuarios.append({
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "email": email,
        "endereco": endereco
    })
    return f"Usuário {nome} criado com sucesso."

def filtrar_usuario(cpf,usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf,usuarios)
    
    if usuarios:
        print("Conta criada com sucesso.")
        return {"agência": agencia, "numero_conta": numero_conta, "usuário": usuario}
    
    print("Usuário não encontrado.")

def listar_contas(contas):
    for conta in contas:
        print(f"Agência: {conta['agência']}")
        print(f"Conta: {conta['numero_conta']}")
        print(f"Usuário: {conta['usuário']['nome']}")
        print()

def main():
    """
    Função principal do sistema bancário.
    """

    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = []
    numero_saques = 0
    usuarios = []
    contas = []

    while True:
        opcao = menu()
        
        if opcao == "1":
            valor = float(input("Digite o valor do saque: "))
            
            saldo, extrato = sacar(
                valor = valor,
                saldo = saldo,
                extrato = extrato,
                limite = limite,
                numero_saques = numero_saques,
                limite_saques = LIMITE_SAQUES
                )
            
        elif opcao == "2":
            valor = float(input("Digite o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "3":
            exibir_extrato(saldo = saldo, extrato = extrato)
        
        elif opcao == "4":
            criar_usuario(usuarios)
        
        elif opcao == "5":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)
            if conta:
                contas.append(conta)
            
        elif opcao == "6":
            listar_contas(contas)
        
        elif opcao == "7":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")

main()

