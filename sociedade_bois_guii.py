import tkinter as tk
from tkinter import messagebox
import json

ARQUIVO = "sociedade_bois.json"


def carregar_dados():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except:
        return []


def salvar_dados():
    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lotes, arquivo, indent=4, ensure_ascii=False)


lotes = carregar_dados()
socios = []


def adicionar_socio():
    try:
        nome = entry_socio.get()
        aporte = float(entry_aporte.get())

        socios.append({
            "nome": nome,
            "aporte": aporte
        })

        lista_socios.insert(
            tk.END,
            f"{nome} - R$ {aporte:.2f}"
        )

        entry_socio.delete(0, tk.END)
        entry_aporte.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Digite um valor válido para o aporte."
        )


def salvar_lote():
    try:
        nome_lote = entry_lote.get()
        fazenda = entry_fazenda.get()
        comprador = entry_comprador.get()

        valor_compra = float(entry_compra.get())
        valor_venda = float(entry_venda.get())
        gastos = float(entry_gastos.get())

        lucro = valor_venda - valor_compra - gastos

        lote = {
            "lote": nome_lote,
            "fazenda": fazenda,
            "comprador": comprador,
            "valor_compra": valor_compra,
            "valor_venda": valor_venda,
            "gastos": gastos,
            "lucro": lucro,
            "socios": socios.copy()
        }

        lotes.append(lote)
        salvar_dados()

        lista_lotes.insert(
            tk.END,
            f"{nome_lote} | Lucro: R$ {lucro:.2f}"
        )

        total_aporte = sum(
            socio["aporte"] for socio in socios
        )

        relatorio = f"Lucro total: R$ {lucro:.2f}\n\n"

        if total_aporte > 0:
            for socio in socios:
                percentual = socio["aporte"] / total_aporte
                valor_receber = lucro * percentual

                relatorio += (
                    f"{socio['nome']} → "
                    f"R$ {valor_receber:.2f}\n"
                )

        messagebox.showinfo(
            "Divisão dos Lucros",
            relatorio
        )

        socios.clear()
        lista_socios.delete(0, tk.END)

    except ValueError:
        messagebox.showerror(
            "Erro",
            "Preencha os campos numéricos corretamente."
        )


root = tk.Tk()
root.title("Sociedade de Bois")
root.geometry("800x700")

tk.Label(root, text="Nome do Lote").pack()
entry_lote = tk.Entry(root, width=40)
entry_lote.pack()

tk.Label(root, text="Fazenda").pack()
entry_fazenda = tk.Entry(root, width=40)
entry_fazenda.pack()

tk.Label(root, text="Comprador").pack()
entry_comprador = tk.Entry(root, width=40)
entry_comprador.pack()

tk.Label(root, text="Valor da Compra").pack()
entry_compra = tk.Entry(root, width=40)
entry_compra.pack()

tk.Label(root, text="Valor da Venda").pack()
entry_venda = tk.Entry(root, width=40)
entry_venda.pack()

tk.Label(root, text="Gastos Totais").pack()
entry_gastos = tk.Entry(root, width=40)
entry_gastos.pack()

tk.Label(root, text="Nome do Sócio").pack()
entry_socio = tk.Entry(root, width=40)
entry_socio.pack()

tk.Label(root, text="Aporte do Sócio").pack()
entry_aporte = tk.Entry(root, width=40)
entry_aporte.pack()

tk.Button(
    root,
    text="Adicionar Sócio",
    command=adicionar_socio
).pack(pady=5)

lista_socios = tk.Listbox(root, width=60)
lista_socios.pack(pady=10)

tk.Button(
    root,
    text="Salvar Lote",
    command=salvar_lote
).pack(pady=10)

tk.Label(root, text="Lotes Cadastrados").pack()

lista_lotes = tk.Listbox(root, width=80)
lista_lotes.pack(fill="both", expand=True)

for lote in lotes:
    nome = lote.get("lote", "Sem nome")
    lucro = lote.get("lucro", 0)

    lista_lotes.insert(
        tk.END,
        f"{nome} | Lucro: R$ {lucro:.2f}"
    )

root.mainloop()