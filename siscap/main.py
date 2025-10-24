from __future__ import annotations

from professor import Professor
from aluno import Aluno
from gerenciador_bd import GerenciadorBD
from controlador_presenca import ControladorPresenca


def main() -> None:
    """Fluxo de demonstração do sistema SISCAP."""

    # Inicializar banco de dados
    bd = GerenciadorBD()
    bd.conectar()
    bd.criar_tabelas()

    # Cadastrar pessoas
    prof = Professor(
        id_=1,
        nome_completo="Profa. Ana Lima",
        disciplina_ministrada="Matemática",
    )
    a1 = Aluno(id_=101, nome_completo="João Silva", turma="1A")
    a2 = Aluno(id_=102, nome_completo="Maria Souza", turma="1A")
    a3 = Aluno(id_=103, nome_completo="Carlos Oliveira", turma="1A")

    bd.salvar_pessoa(prof)
    bd.salvar_pessoa(a1)
    bd.salvar_pessoa(a2)
    bd.salvar_pessoa(a3)

    # Criar controlador
    controlador = ControladorPresenca(bd)

    # Lançar chamadas
    controlador.lancar_chamada_dia("2025-10-22", {101: "Presente", 102: "Presente", 103: "Ausente"})
    controlador.lancar_chamada_dia("2025-10-23", {101: "Presente", 102: "Presente", 103: "Presente"})

    # Consultar e imprimir
    print(controlador.consultar_situacao_dia("2025-10-22"))

    # Desconectar
    bd.desconectar()


if __name__ == "__main__":
    main()
