biblioteca = []

while True:
    print("\n=== SISTEMA DE BIBLIOTECA ===")
    print("1 - Cadastrar livro")
    print("2 - Listar livros")
    print("3 - Emprestar livro")
    print("4 - Devolver livro")
    print("5 - Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        titulo = input("Título do livro: ")
        autor = input("Autor: ")

        livro = {
            "titulo": titulo,
            "autor": autor,
            "disponivel": True
        }

        biblioteca.append(livro)
        print("Livro cadastrado com sucesso!")

    elif opcao == "2":
        if len(biblioteca) == 0:
            print("Nenhum livro cadastrado.")
        else:
            print("\n=== LIVROS ===")
            for i, livro in enumerate(biblioteca):
                status = "Disponível" if livro["disponivel"] else "Emprestado"

                print(f"{i + 1}. {livro['titulo']}")
                print(f"   Autor: {livro['autor']}")
                print(f"   Status: {status}")

    elif opcao == "3":
        if len(biblioteca) == 0:
            print("Nenhum livro cadastrado.")
        else:
            numero = int(input("Número do livro para empréstimo: ")) - 1

            if 0 <= numero < len(biblioteca):
                if biblioteca[numero]["disponivel"]:
                    biblioteca[numero]["disponivel"] = False
                    print("Livro emprestado com sucesso!")
                else:
                    print("Livro já está emprestado.")
            else:
                print("Livro não encontrado.")

    elif opcao == "4":
        if len(biblioteca) == 0:
            print("Nenhum livro cadastrado.")
        else:
            numero = int(input("Número do livro para devolução: ")) - 1

            if 0 <= numero < len(biblioteca):
                if not biblioteca[numero]["disponivel"]:
                    biblioteca[numero]["disponivel"] = True
                    print("Livro devolvido com sucesso!")
                else:
                    print("Este livro já está disponível.")
            else:
                print("Livro não encontrado.")

    elif opcao == "5":
        print("Sistema encerrado.")
        break

    else:
        print("Opção inválida.")