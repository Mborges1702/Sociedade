"""
modelos.py
Define a classe Vaca, que representa cada animal do rebanho
e guarda seu status reprodutivo, corpo lúteo, hormônios aplicados
e eventuais perdas.
"""


class Vaca:
    def __init__(self, id_vaca, lote, status="Não avaliada",
                 corpo_luteo="Não avaliado", obs_corpo_luteo="",
                 data_diagnostico="", hormonios=None, perdas=None):
        self.id_vaca = str(id_vaca)
        self.lote = lote
        self.status = status                    # "Cheia" / "Vazia" / "Não avaliada"
        self.corpo_luteo = corpo_luteo           # "Sim" / "Não" / "Não avaliado"
        self.obs_corpo_luteo = obs_corpo_luteo    # ex: "CL funcional, 20mm"
        self.data_diagnostico = data_diagnostico
        self.hormonios = hormonios if hormonios is not None else []
        self.perdas = perdas if perdas is not None else []

    def registrar_hormonio(self, data, tipo, dose, observacao=""):
        self.hormonios.append({
            "data": data,
            "tipo": tipo,
            "dose": dose,
            "observacao": observacao
        })

    def registrar_perda(self, data, tipo, observacao=""):
        self.perdas.append({
            "data": data,
            "tipo": tipo,          # ex: "Perda embrionária" / "Perda gestacional" / "Aborto"
            "observacao": observacao
        })

    def atualizar_diagnostico(self, status, corpo_luteo, obs_corpo_luteo, data_diagnostico):
        self.status = status
        self.corpo_luteo = corpo_luteo
        self.obs_corpo_luteo = obs_corpo_luteo
        self.data_diagnostico = data_diagnostico

    def to_dict(self):
        return {
            "id_vaca": self.id_vaca,
            "lote": self.lote,
            "status": self.status,
            "corpo_luteo": self.corpo_luteo,
            "obs_corpo_luteo": self.obs_corpo_luteo,
            "data_diagnostico": self.data_diagnostico,
            "hormonios": self.hormonios,
            "perdas": self.perdas
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            id_vaca=dados.get("id_vaca"),
            lote=dados.get("lote", ""),
            status=dados.get("status", "Não avaliada"),
            corpo_luteo=dados.get("corpo_luteo", "Não avaliado"),
            obs_corpo_luteo=dados.get("obs_corpo_luteo", ""),
            data_diagnostico=dados.get("data_diagnostico", ""),
            hormonios=dados.get("hormonios", []),
            perdas=dados.get("perdas", [])
        )

    def __repr__(self):
        return f"Vaca({self.id_vaca}, lote={self.lote}, status={self.status})"
