import json
import os
from datetime import datetime
from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import QDate

class AtividadesController(QObject):
    atividades_atualizadas = Signal()
    
    def __init__(self):
        super().__init__()
        self.arquivo_json = "SOMA/minhas_datas.json"
        self.dados = {"tarefas": [], "atividades_concluidas": {}}
        self.carregar_dados()
    
    def carregar_dados(self):
        try:
            with open(self.arquivo_json, "r", encoding="utf-8") as f:
                self.dados = json.load(f)
                    
            if "tarefas" not in self.dados:
                self.dados["tarefas"] = []
            if "atividades_concluidas" not in self.dados:
                self.dados["atividades_concluidas"] = {}
            
            self.limpar_atividades_orfas()
                
        except FileNotFoundError:
            self.dados = {"tarefas": [], "atividades_concluidas": {}}
            print("AVISO: Arquivo 'minhas_datas.json' não encontrado.")
        except json.JSONDecodeError:
            print("ERRO: Arquivo JSON corrompido. Criando backup e reiniciando.")
            self.criar_backup()
            self.dados = {"tarefas": [], "atividades_concluidas": {}}
    
    def criar_backup(self):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"SOMA/minhas_datas_backup_{timestamp}.json"
            
            if os.path.exists(self.arquivo_json):
                with open(self.arquivo_json, "r", encoding="utf-8") as original:
                    with open(backup_path, "w", encoding="utf-8") as backup:
                        backup.write(original.read())
                print(f"Backup criado: {backup_path}")
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
    
    def salvar_dados(self):
        try:
            with open(self.arquivo_json, "w", encoding="utf-8") as f:
                json.dump(self.dados, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    @property
    def tarefas(self):
        return self.dados.get("tarefas", [])
    
    @property
    def atividades_concluidas(self):
        return self.dados.get("atividades_concluidas", {})
    
    def obter_tarefas_do_dia(self, data):
        data_str = data.toString("dd-MM-yyyy")
        dia_semana = data.dayOfWeek()
        tarefas_do_dia = []
        
        for tarefa in self.tarefas:
            data_tarefa = QDate.fromString(tarefa["date"], "dd-MM-yyyy")
            
            if tarefa["type"] == "single":
                if tarefa["date"] == data_str:
                    tarefas_do_dia.append(tarefa)
            
            elif tarefa["type"] == "daily":
                if data >= data_tarefa:
                    tarefas_do_dia.append(tarefa)
            
            elif tarefa["type"] == "weekly":
                if data_tarefa.dayOfWeek() == dia_semana and data >= data_tarefa:
                    tarefas_do_dia.append(tarefa)
        
        return tarefas_do_dia
    
    def marcar_tarefa_concluida(self, data, descricao_tarefa, concluida=True):
        data_str = data.toString("dd-MM-yyyy")
        
        if data_str not in self.atividades_concluidas:
            self.dados["atividades_concluidas"][data_str] = {}
        
        self.dados["atividades_concluidas"][data_str][descricao_tarefa] = {
            "concluida": concluida,
            "timestamp": datetime.now().isoformat()
        }
        
        self.salvar_dados()
        self.atividades_atualizadas.emit()
    
    def tarefa_esta_concluida(self, data, descricao_tarefa):
        data_str = data.toString("dd-MM-yyyy")
        
        if data_str in self.atividades_concluidas:
            if descricao_tarefa in self.atividades_concluidas[data_str]:
                return self.atividades_concluidas[data_str][descricao_tarefa].get("concluida", False)
        
        return False
    
    def obter_progresso_do_dia(self, data):
        tarefas_do_dia = self.obter_tarefas_do_dia(data)
        
        if not tarefas_do_dia:
            return 0, 0, 100  # sem tarefas = 100% de progresso
        
        total_tarefas = len(tarefas_do_dia)
        tarefas_concluidas = 0
        
        for tarefa in tarefas_do_dia:
            if self.tarefa_esta_concluida(data, tarefa["description"]):
                tarefas_concluidas += 1
        
        progresso = (tarefas_concluidas / total_tarefas) * 100 if total_tarefas > 0 else 0
        
        return tarefas_concluidas, total_tarefas, progresso
    
    def todas_tarefas_concluidas(self, data):
        tarefas_concluidas, total_tarefas, progresso = self.obter_progresso_do_dia(data)
        return total_tarefas > 0 and tarefas_concluidas == total_tarefas
    
    def obter_estatisticas_periodo(self, data_inicio, data_fim):
        total_tarefas = 0
        total_concluidas = 0
        maior_streak = 0
        streak_atual = 0
        
        current_date = data_inicio
        while current_date <= data_fim:
            tarefas_do_dia = self.obter_tarefas_do_dia(current_date)
            
            if tarefas_do_dia:  # Só processar dias que têm tarefas
                total_tarefas += len(tarefas_do_dia)
                
                concluidas_dia = 0
                for tarefa in tarefas_do_dia:
                    if self.tarefa_esta_concluida(current_date, tarefa["description"]):
                        concluidas_dia += 1
                        total_concluidas += 1
                
                # Verificar se o dia foi perfeito (100% concluído)
                if concluidas_dia == len(tarefas_do_dia) and len(tarefas_do_dia) > 0:
                    streak_atual += 1
                    maior_streak = max(maior_streak, streak_atual)
                else:
                    # Só zerar streak se tinha tarefas mas não concluiu todas
                    streak_atual = 0
            # Dias sem tarefas não afetam o streak
            
            current_date = current_date.addDays(1)
        
        # Taxa de conclusão
        taxa_conclusao = (total_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0
        
        return {
            "taxa_conclusao": taxa_conclusao,
            "streak_dias_perfeitos": maior_streak,
            "total_tarefas_concluidas": total_concluidas
        }
    
    def limpar_atividades_orfas(self):
        tarefas_existentes = set()
        
        for tarefa in self.tarefas:
            tarefas_existentes.add(tarefa["description"])
        
        datas_para_remover = []
        alteracoes_feitas = False
        
        for data, atividades_do_dia in self.atividades_concluidas.items():
            atividades_orfas = []
            
            for descricao_atividade in list(atividades_do_dia.keys()):
                if descricao_atividade not in tarefas_existentes:
                    atividades_orfas.append(descricao_atividade)
            
            for atividade_orfa in atividades_orfas:
                del atividades_do_dia[atividade_orfa]
                alteracoes_feitas = True
            
            if not atividades_do_dia:
                datas_para_remover.append(data)
        
        for data in datas_para_remover:
            del self.atividades_concluidas[data]
            alteracoes_feitas = True
        
        if alteracoes_feitas:
            self.salvar_dados()
    
    def obter_eventos_importantes_proximos_30_dias(self):
        data_atual = QDate.currentDate()
        data_limite = data_atual.addDays(30)
        eventos_importantes = []
        
        for tarefa in self.tarefas:
            if tarefa["type"] == "single" and tarefa.get("importante", False):
                data_tarefa = QDate.fromString(tarefa["date"], "dd-MM-yyyy")
                
                if data_atual <= data_tarefa <= data_limite:
                    # Verifica se o evento não está concluído
                    if not self.tarefa_esta_concluida(data_tarefa, tarefa["description"]):
                        dias_restantes = data_atual.daysTo(data_tarefa)
                        eventos_importantes.append({
                            "descricao": tarefa["description"],
                            "data": data_tarefa,
                            "data_str": data_tarefa.toString("dd/MM/yyyy"),
                            "dias_restantes": dias_restantes
                        })
        
        #  Próximos primeiro
        eventos_importantes.sort(key=lambda x: x["data"])
        return eventos_importantes
