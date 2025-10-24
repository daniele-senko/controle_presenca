from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from siscap.gerenciador_bd import GerenciadorBD


class ControladorPresenca:
    """Controlador de presença para gerenciar operações de chamada escolar.

    Intermediário entre a aplicação e o gerenciador de banco de dados.
    """

    def __init__(self, gerenciador_bd: GerenciadorBD) -> None:
        """Inicializa o controlador com um gerenciador de BD.

        Args:
            gerenciador_bd: Instância de GerenciadorBD para persistência.
        """

        self._gerenciador_bd = gerenciador_bd

    def lancar_chamada_dia(self, data_aula: str, status_alunos: dict[int, str]) -> None:
        """Lança chamada para um dia, registrando presença de alunos.

        Args:
            data_aula: Data no formato YYYY-MM-DD.
            status_alunos: Dicionário mapeando id_aluno -> status ('Presente'/'Ausente').

        Raises:
            ValueError: Se dados inválidos forem passados.
        """

        for id_aluno, status in status_alunos.items():
            self._gerenciador_bd.salvar_registro_presenca(id_aluno, data_aula, status)

    def consultar_situacao_dia(self, data_aula: str) -> str:
        """Consulta e formata a situação de presença para um dia.

        Args:
            data_aula: Data no formato YYYY-MM-DD.

        Returns:
            String formatada com a situação da chamada, uma linha por aluno.
            Formato:
                "Situação da chamada - {data_aula}:\\n - {nome} (ID {id_aluno}): {status}"
        """

        registros = self._gerenciador_bd.consultar_registros_por_data(data_aula)

        if not registros:
            return f"Situação da chamada - {data_aula}:\n(Nenhum registro encontrado)"

        linhas = [f"Situação da chamada - {data_aula}:"]
        for id_aluno, nome, status in registros:
            linhas.append(f" - {nome} (ID {id_aluno}): {status}")

        return "\n".join(linhas)
