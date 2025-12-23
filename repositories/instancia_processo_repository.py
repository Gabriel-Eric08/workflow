from models.models import db, InstanciaProcesso, EtapaDefinicao, TarefaExecucao, Funcionario, ModeloProcesso
from datetime import datetime

class InstanciaProcessoReository:
    
    # 1. INICIAR PROCESSO (Agora salvando o nome_processo)
    def iniciar_processo(self, id_modelo, id_criador):
        try:
            # A) Busca o Modelo para pegar o Nome
            modelo = ModeloProcesso.query.get(id_modelo)
            if not modelo:
                return {"sucess": False, "message": "Modelo de processo não encontrado."}

            # B) Cria a Instância já com o NOME DO PROCESSO (Snapshot)
            nova_instancia = InstanciaProcesso(
                id_modelo=id_modelo,
                nome_processo=modelo.nome_processo, # <--- AQUI ESTÁ A MUDANÇA
                id_criador=id_criador,
                status_geral=0, 
                data_inicio=datetime.utcnow()
            )
            db.session.add(nova_instancia)
            db.session.flush() 

            # C) Busca a 1ª Etapa
            primeira_etapa = EtapaDefinicao.query.filter_by(
                id_modelo=id_modelo, 
                ordem_sequencial=1
            ).first()

            if not primeira_etapa:
                db.session.rollback()
                return {"sucess": False, "message": "Este modelo não possui etapas configuradas."}

            # D) Cria a 1ª Tarefa
            primeira_tarefa = TarefaExecucao(
                id_instancia=nova_instancia.id,
                id_etapa_definicao=primeira_etapa.id,
                status_tarefa=0,    
                id_funcionario=None 
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

    # 2. LISTAR TODAS AS INSTÂNCIAS (Para o Dashboard)
    def get_todas_instancias(self):
        try:
            # Agora não precisamos obrigatoriamente do JOIN com ModeloProcesso para pegar o nome
            # Mas ainda fazemos Join com Funcionario para saber quem criou
            instancias = db.session.query(InstanciaProcesso, Funcionario)\
                .outerjoin(Funcionario, InstanciaProcesso.id_criador == Funcionario.id)\
                .order_by(InstanciaProcesso.data_inicio.desc())\
                .all()

            lista_formatada = []
            for inst, func in instancias:
                lista_formatada.append({
                    "id": inst.id,
                    "codigo": f"PRO-{inst.id}", # Exemplo de protocolo visual
                    "nome_processo": inst.nome_processo, # Pegando direto da tabela instancias
                    "criado_por": func.nome if func else "Sistema",
                    "data_inicio": inst.data_inicio.strftime('%d/%m/%Y %H:%M'),
                    "status_cod": inst.status_geral,
                    "status": "Concluído" if inst.status_geral == 1 else "Em Andamento"
                })
            
            return lista_formatada
        except Exception as e:
            print(f"Error listing instancias: {e}")
            return []

    # 3. LISTAR TAREFAS PENDENTES (Mantido igual, mas retornando nome_processo da instancia)
    def get_tarefas_pendentes(self, id_usuario):
        try:
            usuario = Funcionario.query.get(id_usuario)
            if not usuario: return []

            id_meu_cargo = usuario.id_cargo

            tarefas = db.session.query(TarefaExecucao, EtapaDefinicao, InstanciaProcesso)\
                .join(EtapaDefinicao, TarefaExecucao.id_etapa_definicao == EtapaDefinicao.id)\
                .join(InstanciaProcesso, TarefaExecucao.id_instancia == InstanciaProcesso.id)\
                .filter(TarefaExecucao.status_tarefa == 0)\
                .filter(EtapaDefinicao.id_cargo == id_meu_cargo)\
                .all()

            lista = []
            for tarefa, etapa, instancia in tarefas:
                lista.append({
                    "id_tarefa": tarefa.id,
                    "nome_processo": instancia.nome_processo, # Usando o novo campo
                    "id_instancia": instancia.id,
                    "tarefa_atual": etapa.nome_tarefa,
                    "descricao_etapa": etapa.descricao,
                    "data_inicio": instancia.data_inicio.strftime('%d/%m/%Y %H:%M'),
                    "requer_anexo": etapa.requer_anexo,
                    "requer_obs": etapa.requer_obs
                })
            return lista
        except Exception as e:
            return []

    # 4. CONCLUIR TAREFA (Mesma lógica anterior, mantida para contexto)
    def concluir_tarefa(self, id_tarefa, id_usuario, texto_saida=None):
        try:
            tarefa_atual = TarefaExecucao.query.get(id_tarefa)
            if not tarefa_atual: return {"sucess": False, "message": "Tarefa não encontrada"}

            tarefa_atual.status_tarefa = 1 
            tarefa_atual.id_funcionario = id_usuario
            tarefa_atual.texto_saida = texto_saida
            tarefa_atual.data_conclusao = datetime.utcnow()
            
            etapa_atual = tarefa_atual.etapa_definicao
            proxima_etapa = EtapaDefinicao.query.filter_by(
                id_modelo=etapa_atual.id_modelo, 
                ordem_sequencial=etapa_atual.ordem_sequencial + 1
            ).first()

            if proxima_etapa:
                nova_tarefa = TarefaExecucao(
                    id_instancia=tarefa_atual.id_instancia,
                    id_etapa_definicao=proxima_etapa.id,
                    status_tarefa=0 
                )
                db.session.add(nova_tarefa)
                msg = "Tarefa concluída! Próxima etapa gerada."
            else:
                instancia = InstanciaProcesso.query.get(tarefa_atual.id_instancia)
                instancia.status_geral = 1
                msg = "Processo finalizado com sucesso!"

            db.session.commit()
            return {"sucess": True, "message": msg}

        except Exception as e:
            db.session.rollback()
            return {"sucess": False, "message": str(e)}
    
    # 5. NOVO: LISTAR MODELOS (Para preencher o dropdown)
    def get_lista_modelos_simples(self):
        try:
            # Retorna apenas ID e Nome para o select
            return ModeloProcesso.query.with_entities(ModeloProcesso.id, ModeloProcesso.nome_processo).all()
        except Exception:
            return []
    def get_instancia_por_id(self, id_instancia):
        """Busca apenas a instância pelo ID."""
        return InstanciaProcesso.query.get(id_instancia)

    def get_timeline_tarefas(self, id_instancia):
        """
        Busca todas as tarefas (executadas e pendentes) de uma instância,
        trazendo junto os dados da Etapa e do Funcionario (se houver).
        """
        try:
            results = db.session.query(TarefaExecucao, EtapaDefinicao, Funcionario)\
                .join(EtapaDefinicao, TarefaExecucao.id_etapa_definicao == EtapaDefinicao.id)\
                .outerjoin(Funcionario, TarefaExecucao.id_funcionario == Funcionario.id)\
                .filter(TarefaExecucao.id_instancia == id_instancia)\
                .order_by(TarefaExecucao.id.asc())\
                .all()
            return results
        except Exception as e:
            print(f"Erro no repository timeline: {e}")
            return []
            
    def get_usuario_por_id(self, id_usuario):
        """Auxiliar para buscar dados do usuário (para checar cargo)"""
        return Funcionario.query.get(id_usuario)