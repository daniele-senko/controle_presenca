from __future__ import annotations

from abc import ABC, abstractmethod


class Pessoa(ABC):
    """Classe abstrata que representa uma pessoa no domínio SISCAP.

    Atributos privados
    - _id: int
    - _nome_completo: str

    Use as propriedades ``id`` e ``nome_completo`` para acessar e validar
    os valores.
    """

    def __init__(self, id_: int, nome_completo: str) -> None:
        """Inicializa a pessoa.

        Args:
            id_: Identificador numérico positivo.
            nome_completo: Nome completo não vazio.
        """

        self._id: int | None = None
        self._nome_completo: str | None = None
        self.id = id_
        self.nome_completo = nome_completo

    @property
    def id(self) -> int:
        """Retorna o id da pessoa (int > 0)."""

        assert isinstance(self._id, int)
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError(f"id deve ser inteiro, recebido: {type(value).__name__}")
        if value <= 0:
            raise ValueError(f"id deve ser maior que zero, recebido: {value}")
        self._id = value

    @property
    def nome_completo(self) -> str:
        """Retorna o nome completo. Sempre uma string não vazia."""

        assert isinstance(self._nome_completo, str)
        return self._nome_completo

    @nome_completo.setter
    def nome_completo(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"nome_completo deve ser string, recebido: {type(value).__name__}")
        if not value.strip():
            raise ValueError("nome_completo não pode estar vazio")
        self._nome_completo = value.strip()

    @abstractmethod
    def descrever_perfil(self) -> str:  # pragma: no cover - abstract
        """Retorna uma descrição textual do perfil da pessoa.

        Deve ser implementado pelas subclasses (por exemplo, Professor, Aluno).
        """

        raise NotImplementedError()

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(id={self._id!r}, "
            f"nome_completo={self._nome_completo!r})"
        )
