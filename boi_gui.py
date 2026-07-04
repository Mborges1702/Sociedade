import tkinter as tk
from tkinter import messagebox

registros = []


def adicionar():
    try:
        receita = float(entry_receita.get())
        gastos = float(entry_gastos.get())
        despesas = float(entry_despesas.get())

        lucro = receita - (gastos + despesas)
        percentual = (lucro / receita * 100) if receita != 0 else 0

        registros.append({
            "receita": receita,
            "gastos": gastos,
            "despesas": despesas,
            "lucro": lucro,
            "percentual": percentual
        })

        listbox.insert(tk.END, f"Receita: {receita} | Gastos: {gastos} | Despesas: {despesas} | Lucro: {lucro:.2f} ({percentual:.1f}%)")

        entry_receita.delete(0, tk.END)
        entry_gastos.delete(0, tk.END)
        entry_despesas.delete(0, tk.END)
        
        messagebox.showinfo("Sucesso", "Registro adicionado!")

    except ValueError:
        messagebox.showerror("Erro", "Digite apenas números")


def deletar():
    try:
        indice = listbox.curselection()[0]
        listbox.delete(indice)
        registros.pop(indice)
        messagebox.showinfo("Sucesso", "Registro deletado!")
    except IndexError:
        messagebox.showerror("Erro", "Selecione um registro para deletar")


def relatorio():
    if not registros:
        messagebox.showinfo("Relatório", "Nenhum registro encontrado")
        return

    total_receita = sum(r["receita"] for r in registros)
    total_gastos = sum(r["gastos"] for r in registros)
    total_despesas = sum(r["despesas"] for r in registros)
    total_lucro = sum(r["lucro"] for r in registros)
    media_percentual = (total_lucro / total_receita * 100) if total_receita != 0 else 0

    mensagem = f"""
RELATÓRIO GERAL

Total de Registros: {len(registros)}
Receita Total: R$ {total_receita:.2f}
Gastos Total: R$ {total_gastos:.2f}
Despesas Total: R$ {total_despesas:.2f}
Lucro Total: R$ {total_lucro:.2f}
Lucro %: {media_percentual:.2f}%
"""
    messagebox.showinfo("Relatório", mensagem)


def limpar_lista():
    if messagebox.askyesno("Confirmar", "Deseja limpar todos os registros?"):
        listbox.delete(0, tk.END)
        registros.clear()
        messagebox.showinfo("Sucesso", "Lista limpa!")


janela = tk.Tk()
janela.title("Sistema de Bois")
janela.geometry("700x500")

# Frame para entrada
frame_entrada = tk.LabelFrame(janela, text="Entrada de Dados", padx=10, pady=10)
frame_entrada.pack(padx=10, pady=10, fill="x")

tk.Label(frame_entrada, text="Receita:").grid(row=0, column=0, sticky="w")
entry_receita = tk.Entry(frame_entrada, width=15)
entry_receita.grid(row=0, column=1, padx=5)

tk.Label(frame_entrada, text="Gastos:").grid(row=0, column=2, sticky="w")
entry_gastos = tk.Entry(frame_entrada, width=15)
entry_gastos.grid(row=0, column=3, padx=5)

tk.Label(frame_entrada, text="Despesas:").grid(row=0, column=4, sticky="w")
entry_despesas = tk.Entry(frame_entrada, width=15)
entry_despesas.grid(row=0, column=5, padx=5)

# Frame para botões
frame_botoes = tk.Frame(janela)
frame_botoes.pack(padx=10, pady=10, fill="x")

tk.Button(frame_botoes, text="Adicionar", command=adicionar, bg="green", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botoes, text="Deletar", command=deletar, bg="red", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botoes, text="Relatório", command=relatorio, bg="blue", fg="white", width=12).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botoes, text="Limpar", command=limpar_lista, bg="orange", fg="white", width=12).pack(side=tk.LEFT, padx=5)

# Listbox
tk.Label(janela, text="Registros:", font=("Arial", 10, "bold")).pack(padx=10, anchor="w")
listbox = tk.Listbox(janela, width=80, height=15)
listbox.pack(padx=10, pady=10, fill="both", expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(janela)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscroll=scrollbar.set)
scrollbar.config(command=listbox.yview)

janela.mainloop()

janela.mainloop()