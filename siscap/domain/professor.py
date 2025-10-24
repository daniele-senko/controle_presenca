from __future__ import annotations

from .pessoa import Pessoa


class Professor(Pessoa):
    """Representa um professor no sistema SISCAP.

    Herda de Pessoa e adiciona a disciplina ministrada como atributo privado.
    """

    def __init__(
        self, id_: int, nome_completo: str, disciplina_ministrada: str
    ) -> None:
        """Inicializa o professor.

        Args:
            id_: Identificador numérico positivo.
            nome_completo: Nome completo não vazio.
            disciplina_ministrada: Disciplina que o professor ministra (não vazia).
        """

        super().__init__(id_, nome_completo)
        self._disciplina_ministrada: str | None = None
        self.disciplina_ministrada = disciplina_ministrada

    @property
    def disciplina_ministrada(self) -> str:
        """Retorna a disciplina ministrada. Sempre uma string não vazia."""

        assert isinstance(self._disciplina_ministrada, str)
        return self._disciplina_ministrada

    @disciplina_ministrada.setter
    def disciplina_ministrada(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"disciplina_ministrada deve ser string, recebido: {type(value).__name__}")
        if not value.strip():
            raise ValueError("disciplina_ministrada não pode estar vazia")
        self._disciplina_ministrada = value.strip()

    def descrever_perfil(self) -> str:
        """Retorna uma descrição do perfil do professor.

        Returns:
            Descrição no formato: "Professor(a) da disciplina {disciplina_ministrada}"
        """

        return f"Professor(a) da disciplina {self.disciplina_ministrada}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self._id!r}, "
            f"nome_completo={self._nome_completo!r}, "
            f"disciplina_ministrada={self._disciplina_ministrada!r})"
        )
