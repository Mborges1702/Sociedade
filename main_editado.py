"""
main.py
Programa de manejo reprodutivo de rebanho bovino.
Interface Tkinter com abas para:
  - Diagnóstico (cheia / vazia / corpo lúteo)
  - Aplicação de hormônio
  - Registro de perdas
  - Lista de vacas (com filtro por lote)
  - Relatório final (com filtro por lote)

Os dados são persistidos em rebanho.json na mesma pasta.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import os
import tempfile

from modelos import Vaca
from gerenciador import GerenciadorRebanho


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Manejo Reprodutivo do Rebanho")
        self.geometry("780x560")

        self.gerenciador = GerenciadorRebanho()

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        self.aba_cadastro = ttk.Frame(notebook)
        self.aba_hormonio = ttk.Frame(notebook)
        self.aba_perda = ttk.Frame(notebook)
        self.aba_lista = ttk.Frame(notebook)
        self.aba_relatorio = ttk.Frame(notebook)

        notebook.add(self.aba_cadastro, text="Diagnóstico")
        notebook.add(self.aba_hormonio, text="Hormônio")
        notebook.add(self.aba_perda, text="Perdas")
        notebook.add(self.aba_lista, text="Lista de Vacas")
        notebook.add(self.aba_relatorio, text="Relatório")

        self.notebook = notebook
        self.notebook.bind("<<NotebookTabChanged>>", self._ao_trocar_aba)

        self._montar_aba_cadastro()
        self._montar_aba_hormonio()
        self._montar_aba_perda()
        self._montar_aba_lista()
        self._montar_aba_relatorio()

        self._atualizar_tudo()

    # ---------------------------------------------------------------
    # ABA 1: DIAGNÓSTICO (cadastro / cheia / vazia / corpo lúteo)
    # ---------------------------------------------------------------
    def _montar_aba_cadastro(self):
        f = self.aba_cadastro
        pad = {"padx": 6, "pady": 6}

        ttk.Label(f, text="ID da vaca:").grid(row=0, column=0, sticky="e", **pad)
        self.var_id = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_id, width=20).grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(f, text="Lote:").grid(row=1, column=0, sticky="e", **pad)
        self.var_lote = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_lote, width=20).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(f, text="Status reprodutivo:").grid(row=2, column=0, sticky="e", **pad)
        self.var_status = tk.StringVar(value="Não avaliada")
        ttk.Combobox(f, textvariable=self.var_status,
                     values=["Cheia", "Vazia", "Não avaliada"],
                     state="readonly", width=18).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(f, text="Corpo lúteo:").grid(row=3, column=0, sticky="e", **pad)
        self.var_cl = tk.StringVar(value="Não avaliado")
        ttk.Combobox(f, textvariable=self.var_cl,
                     values=["Sim", "Não", "Não avaliado"],
                     state="readonly", width=18).grid(row=3, column=1, sticky="w", **pad)

        ttk.Label(f, text="Obs. corpo lúteo:").grid(row=4, column=0, sticky="e", **pad)
        self.var_obs_cl = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_obs_cl, width=40).grid(row=4, column=1, columnspan=2, sticky="w", **pad)

        ttk.Label(f, text="Data do diagnóstico (dd/mm/aaaa):").grid(row=5, column=0, sticky="e", **pad)
        self.var_data_diag = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        ttk.Entry(f, textvariable=self.var_data_diag, width=20).grid(row=5, column=1, sticky="w", **pad)

        botoes = ttk.Frame(f)
        botoes.grid(row=6, column=0, columnspan=3, pady=12)
        ttk.Button(botoes, text="Salvar / Atualizar", command=self._salvar_diagnostico).pack(side="left", padx=4)
        ttk.Button(botoes, text="Carregar vaca", command=self._carregar_vaca_no_form).pack(side="left", padx=4)
        ttk.Button(botoes, text="Excluir vaca", command=self._excluir_vaca).pack(side="left", padx=4)
        ttk.Button(botoes, text="Limpar formulário", command=self._limpar_form_cadastro).pack(side="left", padx=4)

    def _limpar_form_cadastro(self):
        self.var_id.set("")
        self.var_lote.set("")
        self.var_status.set("Não avaliada")
        self.var_cl.set("Não avaliado")
        self.var_obs_cl.set("")
        self.var_data_diag.set(date.today().strftime("%d/%m/%Y"))

    def _salvar_diagnostico(self):
        id_vaca = self.var_id.get().strip()
        if not id_vaca:
            messagebox.showwarning("Atenção", "Informe o ID da vaca.")
            return

        vaca = self.gerenciador.buscar_vaca(id_vaca)
        if vaca is None:
            vaca = Vaca(id_vaca=id_vaca, lote=self.var_lote.get().strip())

        vaca.lote = self.var_lote.get().strip()
        vaca.atualizar_diagnostico(
            status=self.var_status.get(),
            corpo_luteo=self.var_cl.get(),
            obs_corpo_luteo=self.var_obs_cl.get().strip(),
            data_diagnostico=self.var_data_diag.get().strip()
        )
        self.gerenciador.adicionar_ou_atualizar_vaca(vaca)
        messagebox.showinfo("Sucesso", f"Vaca {id_vaca} salva com sucesso.")
        self._atualizar_tudo()

    def _carregar_vaca_no_form(self):
        id_vaca = self.var_id.get().strip()
        vaca = self.gerenciador.buscar_vaca(id_vaca)
        if vaca is None:
            messagebox.showwarning("Atenção", f"Vaca {id_vaca} não encontrada.")
            return
        self.var_lote.set(vaca.lote)
        self.var_status.set(vaca.status)
        self.var_cl.set(vaca.corpo_luteo)
        self.var_obs_cl.set(vaca.obs_corpo_luteo)
        self.var_data_diag.set(vaca.data_diagnostico)

    def _excluir_vaca(self):
        id_vaca = self.var_id.get().strip()
        if not id_vaca:
            messagebox.showwarning("Atenção", "Informe o ID da vaca.")
            return
        if messagebox.askyesno("Confirmar", f"Excluir a vaca {id_vaca}? Essa ação não pode ser desfeita."):
            if self.gerenciador.remover_vaca(id_vaca):
                messagebox.showinfo("Sucesso", "Vaca excluída.")
                self._limpar_form_cadastro()
                self._atualizar_tudo()
            else:
                messagebox.showwarning("Atenção", "Vaca não encontrada.")

    # ---------------------------------------------------------------
    # ABA 2: HORMÔNIO
    # ---------------------------------------------------------------
    def _montar_aba_hormonio(self):
        f = self.aba_hormonio
        pad = {"padx": 6, "pady": 6}

        ttk.Label(f, text="ID da vaca:").grid(row=0, column=0, sticky="e", **pad)
        self.var_horm_id = tk.StringVar()
        self.combo_horm_id = ttk.Combobox(f, textvariable=self.var_horm_id, width=18, state="normal")
        self.combo_horm_id.grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(f, text="Tipo de hormônio:").grid(row=1, column=0, sticky="e", **pad)
        self.var_horm_tipo = tk.StringVar()
        ttk.Combobox(f, textvariable=self.var_horm_tipo,
                     values=["GnRH", "PGF2alfa (Prostaglandina)", "eCG", "Progesterona (implante)",
                             "Benzoato de Estradiol", "hCG", "Outro"],
                     width=30).grid(row=1, column=1, columnspan=2, sticky="w", **pad)

        ttk.Label(f, text="Dose:").grid(row=2, column=0, sticky="e", **pad)
        self.var_horm_dose = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_horm_dose, width=20).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(f, text="Data (dd/mm/aaaa):").grid(row=3, column=0, sticky="e", **pad)
        self.var_horm_data = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        ttk.Entry(f, textvariable=self.var_horm_data, width=20).grid(row=3, column=1, sticky="w", **pad)

        ttk.Label(f, text="Observação:").grid(row=4, column=0, sticky="e", **pad)
        self.var_horm_obs = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_horm_obs, width=40).grid(row=4, column=1, columnspan=2, sticky="w", **pad)

        ttk.Button(f, text="Registrar aplicação", command=self._registrar_hormonio).grid(
            row=5, column=0, columnspan=3, pady=12)

        ttk.Label(f, text="Histórico da vaca selecionada:").grid(row=6, column=0, columnspan=3, sticky="w", **pad)
        self.texto_horm_hist = tk.Text(f, height=10, width=70)
        self.texto_horm_hist.grid(row=7, column=0, columnspan=3, padx=6, pady=6)
        self.combo_horm_id.bind("<<ComboboxSelected>>", lambda e: self._mostrar_historico_hormonio())

    def _registrar_hormonio(self):
        id_vaca = self.var_horm_id.get().strip()
        vaca = self.gerenciador.buscar_vaca(id_vaca)
        if vaca is None:
            messagebox.showwarning("Atenção", f"Vaca {id_vaca} não encontrada. Cadastre-a na aba Diagnóstico.")
            return
        tipo = self.var_horm_tipo.get().strip()
        if not tipo:
            messagebox.showwarning("Atenção", "Informe o tipo de hormônio.")
            return
        vaca.registrar_hormonio(
            data=self.var_horm_data.get().strip(),
            tipo=tipo,
            dose=self.var_horm_dose.get().strip(),
            observacao=self.var_horm_obs.get().strip()
        )
        self.gerenciador.adicionar_ou_atualizar_vaca(vaca)
        messagebox.showinfo("Sucesso", f"Aplicação registrada para a vaca {id_vaca}.")
        self.var_horm_dose.set("")
        self.var_horm_obs.set("")
        self._mostrar_historico_hormonio()

    def _mostrar_historico_hormonio(self):
        id_vaca = self.var_horm_id.get().strip()
        vaca = self.gerenciador.buscar_vaca(id_vaca)
        self.texto_horm_hist.delete("1.0", tk.END)
        if vaca is None or not vaca.hormonios:
            self.texto_horm_hist.insert(tk.END, "Nenhuma aplicação registrada.")
            return
        for h in vaca.hormonios:
            linha = f"{h['data']} - {h['tipo']} - dose: {h['dose']} - {h.get('observacao', '')}\n"
            self.texto_horm_hist.insert(tk.END, linha)

    # ---------------------------------------------------------------
    # ABA 3: PERDAS
    # ---------------------------------------------------------------
    def _montar_aba_perda(self):
        f = self.aba_perda
        pad = {"padx": 6, "pady": 6}

        ttk.Label(f, text="ID da vaca:").grid(row=0, column=0, sticky="e", **pad)
        self.var_perda_id = tk.StringVar()
        self.combo_perda_id = ttk.Combobox(f, textvariable=self.var_perda_id, width=18, state="normal")
        self.combo_perda_id.grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(f, text="Tipo de perda:").grid(row=1, column=0, sticky="e", **pad)
        self.var_perda_tipo = tk.StringVar(value="Perda embrionária")
        ttk.Combobox(f, textvariable=self.var_perda_tipo,
                     values=["Perda embrionária", "Perda gestacional", "Aborto"],
                     state="readonly", width=25).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(f, text="Data (dd/mm/aaaa):").grid(row=2, column=0, sticky="e", **pad)
        self.var_perda_data = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
        ttk.Entry(f, textvariable=self.var_perda_data, width=20).grid(row=2, column=1, sticky="w", **pad)

        ttk.Label(f, text="Observação:").grid(row=3, column=0, sticky="e", **pad)
        self.var_perda_obs = tk.StringVar()
        ttk.Entry(f, textvariable=self.var_perda_obs, width=40).grid(row=3, column=1, columnspan=2, sticky="w", **pad)

        ttk.Button(f, text="Registrar perda", command=self._registrar_perda).grid(
            row=4, column=0, columnspan=3, pady=12)

        ttk.Label(f, text="Histórico da vaca selecionada:").grid(row=5, column=0, columnspan=3, sticky="w", **pad)
        self.texto_perda_hist = tk.Text(f, height=10, width=70)
        self.texto_perda_hist.grid(row=6, column=0, columnspan=3, padx=6, pady=6)
        self.combo_perda_id.bind("<<ComboboxSelected>>", lambda e: self._mostrar_historico_perda())

    def _registrar_perda(self):
        id_vaca = self.var_perda_id.get().strip()
        vaca = self.gerenciador.buscar_vaca(id_vaca)
        if vaca is None:
            messagebox.showwarning("Atenção", f"Vaca {id_vaca} não encontrada. Cadastre-a na aba Diagnóstico.")
            return
        vaca.registrar_perda(
            data=self.var_perda_data.get().strip(),
            tipo=self.var_perda_tipo.get(),
            observacao=self.var_perda_obs.get().strip()
        )
        # Perda geralmente reclassifica o status da vaca para "Vazia"
        vaca.status = "Vazia"
        self.gerenciador.adicionar_ou_atualizar_vaca(vaca)
        messagebox.showinfo("Sucesso", f"Perda registrada para a vaca {id_vaca}. Status atualizado para 'Vazia'.")
        self.var_perda_obs.set("")
        self._mostrar_historico_perda()
        self._atualizar_tudo()

    def _mostrar_historico_perda(self):
        id_vaca = self.var_perda_id.get().strip()
        vaca = self.gerenciador.buscar_vaca(id_vaca)
        self.texto_perda_hist.delete("1.0", tk.END)
        if vaca is None or not vaca.perdas:
            self.texto_perda_hist.insert(tk.END, "Nenhuma perda registrada.")
            return
        for p in vaca.perdas:
            linha = f"{p['data']} - {p['tipo']} - {p.get('observacao', '')}\n"
            self.texto_perda_hist.insert(tk.END, linha)

    # ---------------------------------------------------------------
    # ABA 4: LISTA DE VACAS
    # ---------------------------------------------------------------
    def _montar_aba_lista(self):
        f = self.aba_lista
        pad = {"padx": 6, "pady": 6}

        topo = ttk.Frame(f)
        topo.pack(fill="x", **pad)
        ttk.Label(topo, text="Filtrar por lote:").pack(side="left")
        ttk.Label(topo, text="Pesquisar:").pack(side="left", padx=(20, 5))
        self.var_filtro_lote_lista = tk.StringVar(value="Todos")
        self.combo_filtro_lista = ttk.Combobox(topo, textvariable=self.var_filtro_lote_lista,
                                                state="readonly", width=20)
        self.combo_filtro_lista.pack(side="left", padx=6)
        self.combo_filtro_lista.bind("<<ComboboxSelected>>", lambda e: self._atualizar_lista())
        ttk.Button(topo, text="Atualizar", command=self._atualizar_lista).pack(side="left", padx=6)

        colunas = ("id", "lote", "status", "corpo_luteo", "data_diag", "hormonios", "perdas")
        self.tree = ttk.Treeview(f, columns=colunas, show="headings", height=18)
        titulos = {"id": "ID", "lote": "Lote", "status": "Status", "corpo_luteo": "Corpo Lúteo",
                   "data_diag": "Data Diagnóstico", "hormonios": "Nº Hormônios", "perdas": "Nº Perdas"}
        larguras = {"id": 70, "lote": 80, "status": 90, "corpo_luteo": 90,
                    "data_diag": 120, "hormonios": 100, "perdas": 80}
        for c in colunas:
            self.tree.heading(c, text=titulos[c])
            self.tree.column(c, width=larguras[c], anchor="center")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

    def _atualizar_lista(self):
        lote = self.var_filtro_lote_lista.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for vaca in self.gerenciador.listar_vacas(lote):
            self.tree.insert("", "end", values=(
                vaca.id_vaca, vaca.lote, vaca.status, vaca.corpo_luteo,
                vaca.data_diagnostico, len(vaca.hormonios), len(vaca.perdas)
            ))

    # ---------------------------------------------------------------
    # ABA 5: RELATÓRIO
    # ---------------------------------------------------------------
    def _montar_aba_relatorio(self):
        f = self.aba_relatorio
        pad = {"padx": 6, "pady": 6}

        topo = ttk.Frame(f)
        topo.pack(fill="x", **pad)
        ttk.Label(topo, text="Lote:").pack(side="left")
        self.var_filtro_lote_relatorio = tk.StringVar(value="Todos")
        self.combo_filtro_relatorio = ttk.Combobox(topo, textvariable=self.var_filtro_lote_relatorio,
                                                    state="readonly", width=20)
        self.combo_filtro_relatorio.pack(side="left", padx=6)
        ttk.Button(topo, text="Gerar relatório", command=self._gerar_relatorio).pack(side="left", padx=6)
        ttk.Button(topo, text="Exportar .txt", command=self._exportar_relatorio).pack(side="left", padx=6)
        ttk.Button(topo, text="Imprimir", command=self._imprimir_relatorio).pack(side="left", padx=6)

        self.texto_relatorio = tk.Text(f, height=24, width=90, font=("Courier New", 10))
        self.texto_relatorio.pack(fill="both", expand=True, padx=6, pady=6)

    def _gerar_relatorio(self):
        lote = self.var_filtro_lote_relatorio.get()
        texto = self.gerenciador.relatorio_texto(lote)
        self.texto_relatorio.delete("1.0", tk.END)
        self.texto_relatorio.insert(tk.END, texto)

    def _exportar_relatorio(self):
        conteudo = self.texto_relatorio.get("1.0", tk.END).strip()
        if not conteudo:
            messagebox.showwarning("Atenção", "Gere o relatório antes de exportar.")
            return
        caminho = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivo de texto", "*.txt")],
            initialfile="relatorio_reprodutivo.txt"
        )
        if caminho:
            with open(caminho, "w", encoding="utf-8") as arq:
                arq.write(conteudo)
            messagebox.showinfo("Sucesso", f"Relatório exportado para:\n{caminho}")

    # ---------------------------------------------------------------
    # Atualizações gerais (combos de lote e ID)
    # ---------------------------------------------------------------
    def _ao_trocar_aba(self, event):
        self._atualizar_tudo()

    def _atualizar_tudo(self):
        lotes = ["Todos"] + self.gerenciador.listar_lotes()
        ids = [v.id_vaca for v in self.gerenciador.listar_vacas()]

        self.combo_filtro_lista["values"] = lotes
        self.combo_filtro_relatorio["values"] = lotes
        self.combo_horm_id["values"] = ids
        self.combo_perda_id["values"] = ids

        self._atualizar_lista()


if __name__ == "__main__":
    app = App()
    app.mainloop()
