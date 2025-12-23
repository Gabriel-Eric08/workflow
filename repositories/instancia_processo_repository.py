from models.models import db, InstanciaProcesso, EtapaDefinicao, TarefaExecucao, Funcionario
from datetime import datetime

class InstanciaProcessoReository:
    
    # 1. INICIAR PROCESSO (Cria a Instância + 1ª Tarefa)
    def iniciar_processo(self, id_modelo, id_criador):
        try:
            # A) Cria a "Pasta" do processo (Instância)
            nova_instancia = InstanciaProcesso(
                id_modelo=id_modelo,
                id_criador=id_criador,
                status_geral=0, # 0 = Em Andamento
                data_inicio=datetime.utcnow()
            )
            db.session.add(nova_instancia)
            db.session.flush() # Necessário para gerar o ID da instância antes do commit

            # B) Busca a 1ª Etapa (Ordem = 1)
            primeira_etapa = EtapaDefinicao.query.filter_by(
                id_modelo=id_modelo, 
                ordem_sequencial=1
            ).first()

            if not primeira_etapa:
                # Se não tiver etapas, faz rollback e avisa
                db.session.rollback()
                return {"sucess": False, "message": "Este modelo não possui etapas configuradas."}

            # C) Cria a 1ª Tarefa na caixa de entrada do cargo responsável
            primeira_tarefa = TarefaExecucao(
                id_instancia=nova_instancia.id,
                id_etapa_definicao=primeira_etapa.id,
                status_tarefa=0,    # 0 = Pendente
                id_funcionario=None # Ninguém pegou ainda
            )
            
            db.session.add(primeira_tarefa)
            db.session.commit()

            return {
                "sucess": True, 
                "message": "Processo iniciado com sucesso!", 
                "id_instancia": nova_instancia.id
            }

        except Exception as e:
            db.session.rollback()
            print(f"Error in repository: {e}")
            return {"sucess": False, "message": str(e)}

    # 2. LISTAR TAREFAS (Baseado no Cargo do Usuário)
    def get_tarefas_pendentes(self, id_usuario):
        try:
            # Descobre o cargo do usuário logado
            usuario = Funcionario.query.get(id_usuario)
            if not usuario:
                return []

            id_meu_cargo = usuario.id_cargo

            # Busca tarefas onde:
            # 1. Status é Pendente (0)
            # 2. O cargo da etapa é igual ao cargo do usuário
            tarefas = db.session.query(TarefaExecucao, EtapaDefinicao, InstanciaProcesso)\
                .join(EtapaDefinicao, TarefaExecucao.id_etapa_definicao == EtapaDefinicao.id)\
                .join(InstanciaProcesso, TarefaExecucao.id_instancia == InstanciaProcesso.id)\
                .filter(TarefaExecucao.status_tarefa == 0)\
                .filter(EtapaDefinicao.id_cargo == id_meu_cargo)\
                .all()

            lista_formatada = []
            for tarefa, etapa, instancia in tarefas:
                lista_formatada.append({
                    "id_tarefa": tarefa.id,
                    "nome_processo": instancia.modelo.nome_processo,
                    "codigo_processo": instancia.modelo.codigo_processo,
                    "id_instancia": instancia.id,
                    "tarefa_atual": etapa.nome_tarefa,
                    "descricao_etapa": etapa.descricao,
                    "data_inicio": instancia.data_inicio.strftime('%d/%m/%Y %H:%M'),
                    "requer_anexo": etapa.requer_anexo,
                    "requer_obs": etapa.requer_obs
                })
            
            return lista_formatada

        except Exception as e:
            print(f"Erro ao buscar tarefas: {e}")
            return []

    # 3. TRAMITAR (Concluir Tarefa -> Gerar Próxima ou Encerrar)
    def concluir_tarefa(self, id_tarefa, id_usuario, texto_saida=None):
        try:
            # A) Carrega a tarefa atual
            tarefa_atual = TarefaExecucao.query.get(id_tarefa)
            if not tarefa_atual:
                return {"sucess": False, "message": "Tarefa não encontrada"}

            # B) Atualiza dados da conclusão
            tarefa_atual.status_tarefa = 1 # Concluído
            tarefa_atual.id_funcionario = id_usuario
            tarefa_atual.texto_saida = texto_saida
            tarefa_atual.data_conclusao = datetime.utcnow()
            
            # C) Lógica de Próximo Passo
            etapa_atual = tarefa_atual.etapa_definicao
            ordem_atual = etapa_atual.ordem_sequencial
            
            # Busca se existe uma etapa com ordem superior (ordem + 1)
            proxima_etapa = EtapaDefinicao.query.filter_by(
                id_modelo=etapa_atual.id_modelo, 
                ordem_sequencial=ordem_atual + 1
            ).first()

            if proxima_etapa:
                # D) GERA A PRÓXIMA TAREFA
                nova_tarefa = TarefaExecucao(
                    id_instancia=tarefa_atual.id_instancia,
                    id_etapa_definicao=proxima_etapa.id,
                    status_tarefa=0 # Pendente para o próximo cargo
                )
                db.session.add(nova_tarefa)
                msg = "Tarefa concluída! O processo avançou para a próxima etapa."
            else:
                # E) ENCERRA O PROCESSO (Não há mais etapas)
                instancia = InstanciaProcesso.query.get(tarefa_atual.id_instancia)
                instancia.status_geral = 1 # Concluído
                msg = "Processo finalizado com sucesso!"

            db.session.commit()
            return {"sucess": True, "message": msg}

        except Exception as e:
            db.session.rollback()
            return {"sucess": False, "message": str(e)}