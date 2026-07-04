saldo = 0
extrato = []

while True:
    print("\n=== SISTEMA BANCÁRIO ===")
    print("1 - Consultar saldo")
    print("2 - Depositar")
    print("3 - Sacar")
    print("4 - Ver extrato")
    print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print(f"\nSaldo atual: R${saldo:.2f}")

    elif opcao == "2":
        valor = float(input("Digite o valor do depósito: R$"))

        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: +R${valor:.2f}")
            print("Depósito realizado com sucesso!")
        else:
            print("Valor inválido.")

    elif opcao == "3":
        valor = float(input("Digite o valor do saque: R$"))

        if valor <= 0:
            print("Valor inválido.")
        elif valor > saldo:
            print("Saldo insuficiente.")
        else:
            saldo -= valor
            extrato.append(f"Saque: -R${valor:.2f}")
            print("Saque realizado com sucesso!")

    elif opcao == "4":
        print("\n=== EXTRATO ===")

        if len(extrato) == 0:
            print("Nenhuma movimentação realizada.")
        else:
            for operacao in extrato:
                print(operacao)

        print(f"\nSaldo atual: R${saldo:.2f}")

    elif opcao == "5":
        print("Encerrando o sistema...")
        break

    else:
        print("Opção inválida. Tente novamente.")