CREATE DATABASE IF NOT EXISTS workflow;
USE workflow;

-- 1. Tabela de Cargos (Quem pode fazer o que)
CREATE TABLE Cargos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_cargo VARCHAR(100) NOT NULL,
    descricao VARCHAR(255)
);

-- 2. Tabela de Funcionários (As pessoas)
CREATE TABLE Funcionarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_cargo INT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE, -- UNIQUE garante que não repita email
    senha_hash TEXT,
    ativo TINYINT(1) DEFAULT 1, -- Usamos TINYINT para booleano (0 ou 1)
    
    -- Relação: O funcionário deve ter um cargo válido
    CONSTRAINT fk_func_cargo FOREIGN KEY (id_cargo) REFERENCES Cargos(id)
);

-- 3. Tabela de Definição do Processo (O "Molde")
CREATE TABLE Modelos_processos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nome_processo VARCHAR(255) NOT NULL,
    codigo_processo VARCHAR(40) UNIQUE, -- Ex: PROC-RH-01
    descricao TEXT
);

-- 4. Tabela de Etapas (O Fluxograma desenhado)
CREATE TABLE Etapas_definicao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_modelo INT,
    id_cargo INT, -- Qual cargo é dono desta etapa?
    nome_tarefa VARCHAR(100),
    ordem_sequencial INT,
    requer_anexo TINYINT(1) DEFAULT 0, -- 0 = Não, 1 = Sim
    requer_obs TINYINT(1) DEFAULT 0,
    
    -- Relações
    CONSTRAINT fk_etapa_modelo FOREIGN KEY (id_modelo) REFERENCES Modelos_processos(id),
    CONSTRAINT fk_etapa_cargo FOREIGN KEY (id_cargo) REFERENCES Cargos(id)
);

-- 5. Tabela de Instâncias (O processo rodando na prática)
CREATE TABLE Instancias_processos (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_modelo INT,
    id_criador INT, -- Quem abriu o processo (um funcionário)
    data_inicio DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_geral INT DEFAULT 0, -- 0: Andamento, 1: Concluído, 2: Cancelado
    
    -- Relações
    CONSTRAINT fk_inst_modelo FOREIGN KEY (id_modelo) REFERENCES Modelos_processos(id),
    CONSTRAINT fk_inst_criador FOREIGN KEY (id_criador) REFERENCES Funcionarios(id)
);

-- 6. Tabela de Tarefas Executadas (O histórico do trabalho)
CREATE TABLE Tarefas_execucao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_instancia INT,
    id_etapa_definicao INT, -- Link para saber qual era a regra dessa tarefa
    id_funcionario INT, -- Quem executou (ou está atribuído)
    status_tarefa INT DEFAULT 0, -- 0: Pendente, 1: Concluída, 2: Erro
    texto_saida TEXT,
    data_conclusao DATETIME,
    
    -- Relações
    CONSTRAINT fk_tarefa_instancia FOREIGN KEY (id_instancia) REFERENCES Instancias_processos(id),
    CONSTRAINT fk_tarefa_etapa FOREIGN KEY (id_etapa_definicao) REFERENCES Etapas_definicao(id),
    CONSTRAINT fk_tarefa_func FOREIGN KEY (id_funcionario) REFERENCES Funcionarios(id)
);

-- 7. Tabela de Anexos (Arquivos das tarefas)
CREATE TABLE Anexos_tarefa (
    id INT PRIMARY KEY AUTO_INCREMENT,
    id_tarefa_executada INT,
    nome_arquivo VARCHAR(255),
    url_arquivo TEXT,
    data_upload DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Relação
    CONSTRAINT fk_anexo_tarefa FOREIGN KEY (id_tarefa_executada) REFERENCES Tarefas_execucao(id)
);