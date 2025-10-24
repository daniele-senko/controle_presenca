from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from siscap.domain.pessoa import Pessoa


class GerenciadorBD:
    """Gerenciador de banco de dados SQLite para SISCAP.

    Responsável por conectar, desconectar, criar tabelas e executar
    operações CRUD de pessoas e registros de presença.
    """

    def __init__(self) -> None:
        """Inicializa o gerenciador usando siscap.db na raiz do projeto."""

        _root = Path(__file__).resolve().parents[2]
        self._db_path = str(_root / "siscap.db")
        self._conn: sqlite3.Connection | None = None

    def conectar(self) -> None:
        """Abre conexão com o banco de dados e configura PRAGMA.

        Usa journal_mode=DELETE para evitar arquivos auxiliares (-wal, -shm).
        """

        self._conn = sqlite3.connect(self._db_path)
        self._conn.row_factory = sqlite3.Row
        with self._conn:
            self._conn.execute("PRAGMA foreign_keys = ON;")
            self._conn.execute("PRAGMA journal_mode = DELETE;")
            self._conn.execute("PRAGMA synchronous = NORMAL;")
            self._conn.execute("PRAGMA temp_store = MEMORY;")

    def desconectar(self) -> None:
        """Fecha a conexão com o banco de dados."""

        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def criar_tabelas(self) -> None:
        """Cria as tabelas Pessoas e RegistrosPresenca se não existirem."""

        if self._conn is None:
            raise RuntimeError("Conexão não estabelecida. Chame conectar() primeiro.")

        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Pessoas (
                    id INTEGER PRIMARY KEY,
                    nome TEXT NOT NULL,
                    tipo_pessoa TEXT NOT NULL CHECK(tipo_pessoa IN ('Professor','Aluno')),
                    disciplina TEXT NULL,
                    turma TEXT NULL
                );
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS RegistrosPresenca (
                    id_registro INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_aluno_fk INTEGER NOT NULL,
                    data_aula TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('Presente','Ausente')),
                    FOREIGN KEY(id_aluno_fk) REFERENCES Pessoas(id)
                );
                """
            )

    def salvar_pessoa(self, pessoa: Pessoa) -> None:
        """Salva uma pessoa (Professor ou Aluno) no banco de dados.

        Args:
            pessoa: Instância de Professor ou Aluno.

        Raises:
            ValueError: Se o tipo de pessoa for inválido.
            sqlite3.IntegrityError: Se o ID já existe ou há outro erro de integridade.
        """

        if self._conn is None:
            raise RuntimeError("Conexão não estabelecida. Chame conectar() primeiro.")

        tipo = pessoa.descrever_perfil()
        tipo_pessoa = "Professor" if "Professor" in tipo else "Aluno"

        if tipo_pessoa not in ("Professor", "Aluno"):
            raise ValueError(f"Tipo de pessoa inválido: {tipo_pessoa}")

        disciplina = None
        turma = None

        # Importação local para evitar ciclo
        from siscap.domain.professor import Professor
        from siscap.domain.aluno import Aluno

        if isinstance(pessoa, Professor):
            tipo_pessoa = "Professor"
            disciplina = pessoa.disciplina_ministrada
        elif isinstance(pessoa, Aluno):
            tipo_pessoa = "Aluno"
            turma = pessoa.turma
        else:
            raise ValueError(f"Tipo de pessoa não reconhecido: {type(pessoa)}")

        try:
            with self._conn:
                self._conn.execute(
                    """
                    INSERT INTO Pessoas (id, nome, tipo_pessoa, disciplina, turma)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (pessoa.id, pessoa.nome_completo, tipo_pessoa, disciplina, turma),
                )
        except sqlite3.IntegrityError as e:
            raise ValueError(f"ID já cadastrado: {pessoa.id}") from e

    def salvar_registro_presenca(
        self, id_aluno: int, data_aula: str, status: str
    ) -> None:
        """Registra presença ou ausência de um aluno em uma data.

        Args:
            id_aluno: ID do aluno.
            data_aula: Data no formato YYYY-MM-DD.
            status: 'Presente' ou 'Ausente'.

        Raises:
            ValueError: Se formato de data inválido, status inválido,
                        ou ID não corresponde a um aluno.
        """

        if self._conn is None:
            raise RuntimeError("Conexão não estabelecida. Chame conectar() primeiro.")

        # Validar formato de data
        if not self._validar_data_aula(data_aula):
            raise ValueError("Data inválida, use YYYY-MM-DD")

        # Validar status
        if status not in ("Presente", "Ausente"):
            raise ValueError(f"Status inválido: {status}. Use 'Presente' ou 'Ausente'.")

        # Garantir que id_aluno é um aluno
        with self._conn:
            cursor = self._conn.execute(
                "SELECT tipo_pessoa FROM Pessoas WHERE id = ?",
                (id_aluno,),
            )
            row = cursor.fetchone()

            if row is None:
                raise ValueError(f"Aluno com ID {id_aluno} não encontrado.")

            if row["tipo_pessoa"] != "Aluno":
                raise ValueError(
                    f"Somente alunos podem receber presença: ID {id_aluno}"
                )

            # Inserir registro de presença
            self._conn.execute(
                """
                INSERT INTO RegistrosPresenca (id_aluno_fk, data_aula, status)
                VALUES (?, ?, ?)
                """,
                (id_aluno, data_aula, status),
            )

    def consultar_registros_por_data(self, data_aula: str) -> list[tuple[int, str, str]]:
        """Consulta registros de presença para uma data específica.

        Args:
            data_aula: Data no formato YYYY-MM-DD.

        Returns:
            Lista de tuplas (id_aluno, nome_aluno, status) ordenada por id_aluno.
        """

        if self._conn is None:
            raise RuntimeError("Conexão não estabelecida. Chame conectar() primeiro.")

        with self._conn:
            cursor = self._conn.execute(
                """
                SELECT p.id, p.nome, rp.status
                FROM RegistrosPresenca rp
                JOIN Pessoas p ON rp.id_aluno_fk = p.id
                WHERE rp.data_aula = ?
                ORDER BY p.id ASC
                """,
                (data_aula,),
            )
            rows = cursor.fetchall()
            return [(row["id"], row["nome"], row["status"]) for row in rows]

    @staticmethod
    def _validar_data_aula(data_aula: str) -> bool:
        """Valida se a data está no formato YYYY-MM-DD."""

        if len(data_aula) != 10:
            return False
        partes = data_aula.split("-")
        if len(partes) != 3:
            return False
        try:
            ano = int(partes[0])
            mes = int(partes[1])
            dia = int(partes[2])
            return 1000 <= ano <= 9999 and 1 <= mes <= 12 and 1 <= dia <= 31
        except ValueError:
            return False
