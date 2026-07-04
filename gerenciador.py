"""
gerenciador.py
Classe responsável por manter o rebanho em memória, salvar/carregar
os dados em JSON e gerar o relatório de vacas cheias, vazias,
corpo lúteo, perdas e hormônios aplicados.
"""

import json
import os
from modelos import Vaca

ARQUIVO_DADOS = "rebanho.json"


class GerenciadorRebanho:
    def __init__(self, arquivo=ARQUIVO_DADOS):
        self.arquivo = arquivo
        self.vacas = {}  # id_vaca -> objeto Vaca
        self.carregar()

    # ---------- CRUD básico ----------

    def adicionar_ou_atualizar_vaca(self, vaca: Vaca):
        self.vacas[vaca.id_vaca] = vaca
        self.salvar()

    def remover_vaca(self, id_vaca):
        id_vaca = str(id_vaca)
        if id_vaca in self.vacas:
            del self.vacas[id_vaca]
            self.salvar()
            return True
        return False

    def buscar_vaca(self, id_vaca):
        return self.vacas.get(str(id_vaca))

    def listar_vacas(self, lote=None):
        vacas = list(self.vacas.values())
        if lote and lote != "Todos":
            vacas = [v for v in vacas if v.lote == lote]
        return sorted(vacas, key=lambda v: v.id_vaca)

    def listar_lotes(self):
        lotes = sorted(set(v.lote for v in self.vacas.values() if v.lote))
        return lotes

    # ---------- Persistência ----------

    def salvar(self):
        dados = {id_vaca: vaca.to_dict() for id_vaca, vaca in self.vacas.items()}
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def carregar(self):
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
            self.vacas = {id_vaca: Vaca.from_dict(v) for id_vaca, v in dados.items()}
        else:
            self.vacas = {}

    # ---------- Relatório ----------

    def gerar_relatorio(self, lote=None):
        vacas = self.listar_vacas(lote)

        total = len(vacas)
        cheias = [v for v in vacas if v.status == "Cheia"]
        vazias = [v for v in vacas if v.status == "Vazia"]
        nao_avaliadas = [v for v in vacas if v.status == "Não avaliada"]

        com_cl = [v for v in vacas if v.corpo_luteo == "Sim"]
        sem_cl = [v for v in vacas if v.corpo_luteo == "Não"]

        total_perdas = sum(len(v.perdas) for v in vacas)
        vacas_com_perda = [v for v in vacas if len(v.perdas) > 0]

        total_aplicacoes_hormonio = sum(len(v.hormonios) for v in vacas)
        vacas_com_hormonio = [v for v in vacas if len(v.hormonios) > 0]

        return {
            "lote": lote if lote else "Todos",
            "total_vacas": total,
            "cheias": len(cheias),
            "vazias": len(vazias),
            "nao_avaliadas": len(nao_avaliadas),
            "com_corpo_luteo": len(com_cl),
            "sem_corpo_luteo": len(sem_cl),
            "total_perdas": total_perdas,
            "qtd_vacas_com_perda": len(vacas_com_perda),
            "total_aplicacoes_hormonio": total_aplicacoes_hormonio,
            "qtd_vacas_com_hormonio": len(vacas_com_hormonio),
            "lista_cheias": [v.id_vaca for v in cheias],
            "lista_vazias": [v.id_vaca for v in vazias],
            "lista_perdas": [(v.id_vaca, p) for v in vacas_com_perda for p in v.perdas],
            "lista_hormonios": [(v.id_vaca, h) for v in vacas_com_hormonio for h in v.hormonios],
        }

    def relatorio_texto(self, lote=None):
        r = self.gerar_relatorio(lote)
        linhas = []
        linhas.append("=" * 50)
        linhas.append(f"RELATÓRIO REPRODUTIVO — Lote: {r['lote']}")
        linhas.append("=" * 50)
        linhas.append(f"Total de vacas avaliadas: {r['total_vacas']}")
        linhas.append(f"  Cheias:         {r['cheias']}")
        linhas.append(f"  Vazias:         {r['vazias']}")
        linhas.append(f"  Não avaliadas:  {r['nao_avaliadas']}")
        linhas.append("-" * 50)
        linhas.append(f"Com corpo lúteo:    {r['com_corpo_luteo']}")
        linhas.append(f"Sem corpo lúteo:    {r['sem_corpo_luteo']}")
        linhas.append("-" * 50)
        linhas.append(f"Total de perdas registradas: {r['total_perdas']} "
                       f"(em {r['qtd_vacas_com_perda']} vaca(s))")
        for id_vaca, p in r["lista_perdas"]:
            linhas.append(f"  - Vaca {id_vaca}: {p['tipo']} em {p['data']} "
                           f"({p.get('observacao', '')})")
        linhas.append("-" * 50)
        linhas.append(f"Total de aplicações de hormônio: {r['total_aplicacoes_hormonio']} "
                       f"(em {r['qtd_vacas_com_hormonio']} vaca(s))")
        for id_vaca, h in r["lista_hormonios"]:
            linhas.append(f"  - Vaca {id_vaca}: {h['tipo']} ({h['dose']}) em {h['data']} "
                           f"({h.get('observacao', '')})")
        linhas.append("=" * 50)
        return "\n".join(linhas)
