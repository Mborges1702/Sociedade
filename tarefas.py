tarefas = []

def mostrar_menu():
    print("\n=== GERENCIADOR DE TAREFAS ===")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Marcar como concluída")
    print("4. Remover tarefa")
    print("5. Sair")
    print("==============================")

def adicionar_tarefa():
    tarefa = input("Digite a nova tarefa: ")
    tarefas.append({"descricao": tarefa, "concluida": False})
    print("✓ Tarefa adicionada!")

def listar_tarefas():
    if len(tarefas) == 0:
        print("Nenhuma tarefa ainda!")
    else:
        print("\n=== SUAS TAREFAS ===")
        for i, tarefa in enumerate(tarefas):
            status = "✓ FEITA" if tarefa["concluida"] else "○ PENDENTE"
            print(f"{i+1}. [{status}] {tarefa['descricao']}")

def marcar_concluida():
    listar_tarefas()
    if len(tarefas) > 0:
        numero = int(input("Qual tarefa concluiu? (número): ")) - 1
        tarefas[numero]["concluida"] = True
        print("✓ Tarefa marcada como concluída!")

def remover_tarefa():
    listar_tarefas()
    if len(tarefas) > 0:
        numero = int(input("Qual tarefa remover? (número): ")) - 1
        tarefas.pop(numero)
        print("✓ Tarefa removida!")

while True:
    mostrar_menu()
    opcao = input("Escolha uma opção (1-5): ")
    
    if opcao == "1":
        adicionar_tarefa()
    elif opcao == "2":
        listar_tarefas()
    elif opcao == "3":
        marcar_concluida()
    elif opcao == "4":
        remover_tarefa()
    elif opcao == "5":
        print("Até logo!")
        break
    else:
        print("Opção inválida!")