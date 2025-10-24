from __future__ import annotations

from pessoa import Pessoa


class Aluno(Pessoa):
    """Representa um aluno no sistema SISCAP.

    Herda de Pessoa e adiciona a turma como atributo privado.
    """

    def __init__(self, id_: int, nome_completo: str, turma: str) -> None:
        """Inicializa o aluno.

        Args:
            id_: Identificador numérico positivo.
            nome_completo: Nome completo não vazio.
            turma: Turma do aluno (não vazia).
        """

        super().__init__(id_, nome_completo)
        self._turma: str | None = None
        self.turma = turma

    @property
    def turma(self) -> str:
        """Retorna a turma do aluno. Sempre uma string não vazia."""

        assert isinstance(self._turma, str)
        return self._turma

    @turma.setter
    def turma(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"turma deve ser string, recebido: {type(value).__name__}")
        if not value.strip():
            raise ValueError("turma não pode estar vazia")
        self._turma = value.strip()

    def descrever_perfil(self) -> str:
        """Retorna uma descrição do perfil do aluno.

        Returns:
            Descrição no formato: "Aluno(a) da turma {turma}"
        """

        return f"Aluno(a) da turma {self.turma}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self._id!r}, "
            f"nome_completo={self._nome_completo!r}, "
            f"turma={self._turma!r})"
        )
