from models.models import TarefaExecucao, db

class TarefaExecucaoRepository:
    def create(self, id_instancia, id_etapa_definicao, id_funcionario, status_tarefa, texto_saida, data_conclusao):
        try:    
            nova_tarefa_execucao = TarefaExecucao(
                id_instancia=id_instancia,
                id_etapa_definicao=id_etapa_definicao,
                id_funcionario=id_funcionario,
                status_tarefa=status_tarefa,
                texto_saida=texto_saida,
                data_conclusao=data_conclusao
            )
            db.session.add(nova_tarefa_execucao)
            db.session.flush()
            return True
        except Exception as e:
            print(f'Error in repository: {e}')
            return False