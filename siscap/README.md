# SISCAP - Sistema de Controle de Presença Escolar

## Descrição

Sistema educacional para controle de presença em Python 3.13, implementando os conceitos de POO com arquitetura em camadas e persistência via SQLite.

## Requisitos

- Python 3.13+
- Nenhuma dependência externa

## Estrutura

```
siscap/
├── domain/
│   ├── pessoa.py
│   ├── professor.py
│   └── aluno.py
├── infra/
│   └── gerenciador_bd.py
├── app/
│   └── controlador_presenca.py
└── main.py
```

## Como Executar

```bash
python -m siscap.main
```

## Saída Esperada

```
Situação da chamada - 2025-10-22:
 - João Silva (ID 101): Presente
 - Maria Souza (ID 102): Presente
 - Carlos Oliveira (ID 103): Ausente
```

## Conceitos de POO

1. **Abstração**: Classe abstrata `Pessoa` com método abstrato `descrever_perfil()`
2. **Encapsulamento**: Atributos privados com validação via @property
3. **Herança**: `Professor` e `Aluno` herdam de `Pessoa`
4. **Polimorfismo**: `descrever_perfil()` com comportamentos diferentes

## Banco de Dados

- **Arquivo**: `siscap.db` (raiz do projeto)
- **Modo**: DELETE journal (sem arquivos auxiliares)
- **Tabelas**: Pessoas, RegistrosPresenca
- **Acesso**: Centralizado via `GerenciadorBD`
```

**Por que `DELETE` e não `WAL`?**
- ✅ **DELETE**: Sem arquivos auxiliares (`-wal`, `-shm`). Apenas `siscap.db` após operação
- ❌ **WAL**: Cria `siscap.db-wal` e `siscap.db-shm` durante operações (mais rápido, mais arquivos)

### Garantia: Nenhum Arquivo Extra

O gerenciador de banco de dados valida após cada operação que **apenas** `siscap.db` existe:

```python
def verificar_db_unico(self) -> None:
    """Valida que nenhum arquivo auxiliar (-journal, -wal, -shm) existe"""
    _ROOT = Path(__file__).resolve().parents[2]
    arquivos_extras = list(_ROOT.glob("siscap.db-*"))
    
    if arquivos_extras:
        raise RuntimeError(
            f"Arquivos extras detectados: {arquivos_extras}. "
            "Apenas siscap.db permitido."
        )
```

### Como Verificar

#### Método 1: Após executar o sistema

```bash
# Terminal 1: Executar o sistema
python siscap/main.py

# Terminal 2: Listar arquivos BD
ls -lah siscap.db*
```

**Saída esperada:**
```
siscap.db    16K
```

**Saída incorreta (não deve ocorrer):**
```
siscap.db        16K
siscap.db-journal (não deve aparecer)
siscap.db-wal     (não deve aparecer)
siscap.db-shm     (não deve aparecer)
```

#### Método 2: Validar centralização de acesso

```bash
# Verificar que sqlite3.connect só existe em gerenciador_bd.py
grep -r "sqlite3.connect" siscap/ | grep -v "gerenciador_bd.py"
# Resultado esperado: (vazio, sem matches)
```

#### Método 3: Inspecionar arquivo BD

```bash
# Ver tamanho e data
ls -lh siscap.db

# Ver conteúdo (esquema)
sqlite3 siscap.db ".schema"
```

**Tabelas esperadas:**
- `Pessoas`: Professores e alunos cadastrados
- `RegistrosPresenca`: Registros de presença/ausência

### Importante: Não Fazer

❌ **Não use caminhos alternativos:**
```python
GerenciadorBD("/tmp/outro.db")     # ❌ Errado
GerenciadorBD(":memory:")          # ❌ Errado
GerenciadorBD("../banco.db")       # ❌ Errado
```

✅ **Use sempre:**
```python
GerenciadorBD()                    # ✅ Correto (usa ./siscap.db)
```

### Teste de Isolamento

Testes usam banco de dados **temporário e isolado** (não contaminam `siscap.db`):

```bash
pytest siscap/tests/ -v
# Resultado: 26 passed
# Saída: siscap.db inalterado após testes
```

---

## Como Rodar

### Requisitos
- Python 3.13+
- Sistema operacional: Linux, macOS ou Windows

### Passo 1: Clonar/acessar o diretório
```bash
cd /caminho/para/SISCAP
```

### Passo 2: Criar e ativar ambiente virtual (opcional, mas recomendado)
```bash
python -m venv .venv
```

**No Linux/macOS:**
```bash
source .venv/bin/activate
```

**No Windows:**
```bash
.venv\Scripts\activate
```

### Passo 3: Executar o script principal
```bash
python siscap/main.py
```

### Saída Esperada

Quando você executar `python siscap/main.py`, verá:

```
--- Teste de validação: nome vazio ---
Erro esperado capturado: nome_completo não pode estar vazio

--- Situação da chamada ---
Situação da chamada - 2025-10-22:
 - João Silva (ID 101): Presente
 - Maria Souza (ID 102): Presente
 - Carlos Oliveira (ID 103): Ausente
```

## Conceitos de Programação Orientada a Objetos

SISCAP implementa os 4 pilares da POO:

### 1. **Abstração**
Define a interface geral do sistema escondendo complexidade.

**Onde aparece:**
- Classe abstrata `Pessoa` em `domain/pessoa.py`
- Método abstrato `descrever_perfil()` obriga subclasses a implementarem comportamento específico
- `GerenciadorBD` em `infra/gerenciador_bd.py` abstrai operações SQLite

**Exemplo:**
```python
from abc import ABC, abstractmethod

class Pessoa(ABC):
    @abstractmethod
    def descrever_perfil(self) -> str:
        raise NotImplementedError()
```

### 2. **Encapsulamento**
Protege dados internos com atributos privados e acesso controlado via properties.

**Onde aparece:**
- Atributos privados: `_id`, `_nome_completo` em `Pessoa`
- Properties com validação: `@property id` e `@id.setter`
- Mensagens de erro claras quando validação falha

**Exemplo:**
```python
class Pessoa(ABC):
    def __init__(self, id_: int, nome_completo: str):
        self._id = None
        self._nome_completo = None
        self.id = id_  # Usa setter para validar
        self.nome_completo = nome_completo

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if value <= 0:
            raise ValueError(f"id deve ser maior que zero, recebido: {value}")
        self._id = value
```

### 3. **Herança**
Reutilização de código através de hierarquia de classes.

**Onde aparece:**
- `Professor` herda de `Pessoa` em `domain/professor.py`
- `Aluno` herda de `Pessoa` em `domain/aluno.py`
- Ambas reutilizam validação de `id` e `nome_completo` da classe base

**Exemplo:**
```python
class Professor(Pessoa):
    def __init__(self, id_: int, nome_completo: str, disciplina_ministrada: str):
        super().__init__(id_, nome_completo)  # Herança
        self._disciplina_ministrada = None
        self.disciplina_ministrada = disciplina_ministrada

class Aluno(Pessoa):
    def __init__(self, id_: int, nome_completo: str, turma: str):
        super().__init__(id_, nome_completo)  # Herança
        self._turma = None
        self.turma = turma
```

### 4. **Polimorfismo**
Mesma interface, comportamentos diferentes em subclasses.

**Onde aparece:**
- Método abstrato `descrever_perfil()` tem implementações diferentes em `Professor` e `Aluno`
- `GerenciadorBD.salvar_pessoa()` aceita `Pessoa` (Professor ou Aluno) e se adapta

**Exemplo:**
```python
# Em Professor
def descrever_perfil(self) -> str:
    return f"Professor(a) da disciplina {self.disciplina_ministrada}"

# Em Aluno
def descrever_perfil(self) -> str:
    return f"Aluno(a) da turma {self.turma}"

# Polimorfismo em ação
pessoas: list[Pessoa] = [prof, aluno]
for pessoa in pessoas:
    print(pessoa.descrever_perfil())  # Diferentes respostas
```

## Fluxo do Sistema

1. **Inicialização**: Conecta ao banco SQLite e cria tabelas
2. **Cadastro**: Insere professor e alunos no banco
3. **Lançamento de Chamada**: Registra presença/ausência por data
4. **Consulta**: Recupera registros de presença ordenados por ID
5. **Formatação**: Retorna string bem formatada para impressão

## Tecnologias

- **Linguagem**: Python 3.13+
- **Banco de Dados**: SQLite 3 (built-in)
- **Padrão de Arquitetura**: Clean Architecture (Domain → Infrastructure → Application)
- **Dependências Externas**: Nenhuma

## Exemplo de Uso Programático

```python
from siscap.domain.professor import Professor
from siscap.domain.aluno import Aluno
from siscap.infra.gerenciador_bd import GerenciadorBD
from siscap.app.controlador_presenca import ControladorPresenca

# Inicializar
bd = GerenciadorBD("siscap.db")
bd.conectar()
bd.criar_tabelas()

# Cadastrar pessoas
prof = Professor(id_=1, nome_completo="Prof. João", disciplina_ministrada="Física")
aluno = Aluno(id_=101, nome_completo="Maria", turma="2B")

bd.salvar_pessoa(prof)
bd.salvar_pessoa(aluno)

# Lançar chamada
controlador = ControladorPresenca(bd)
controlador.lancar_chamada_dia("2025-10-22", {101: "Presente"})

# Consultar
resultado = controlador.consultar_situacao_dia("2025-10-22")
print(resultado)

# Desconectar
bd.desconectar()
```

## Tratamento de Erros

O sistema valida todos os dados de entrada e retorna mensagens de erro claras:

- ✅ `ValueError: id deve ser maior que zero, recebido: -1`
- ✅ `ValueError: nome_completo não pode estar vazio`
- ✅ `ValueError: ID já cadastrado: 1`
- ✅ `ValueError: Data inválida, use YYYY-MM-DD`
- ✅ `ValueError: Somente alunos podem receber presença: ID 1`

## Autor

Desenvolvido como exemplo de arquitetura POO limpa em Python 3.13.

---

**Data**: 23 de outubro de 2025
