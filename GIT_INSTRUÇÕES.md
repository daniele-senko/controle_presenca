# 🚀 INSTRUÇÕES - SUBIR NO GIT REMOTO

## ✅ Estado Atual

- **Repositório Local**: Inicializado ✓
- **Branch**: `main` ✓
- **Commit**: `8114918` - Initial commit (SISCAP project) ✓
- **Status**: `working tree clean` ✓

---

## 📍 Próximas Etapas

### 1️⃣ Escolha o Serviço (GitHub, GitLab, etc)

Você pode usar qualquer um destes serviços:

- **GitHub** (gratuito, mais popular)
- **GitLab** (gratuito, com CI/CD)
- **Gitea** (self-hosted, local)
- **Azure DevOps**
- Outro repositório remoto

### 2️⃣ Crie um Repositório Remoto Vazio

Exemplo no GitHub:
1. Acesse https://github.com/new
2. Nome: `SISCAP`
3. Descrição: `Sistema de Chamadas Acadêmicas - POO + SQLite`
4. Deixe privado ou público conforme preferência
5. **Não** inicialize com README, .gitignore, ou LICENSE
6. Clique em "Create repository"

### 3️⃣ Adicione o Remoto e Faça Push

#### Opção A: HTTPS (mais simples)
```bash
cd /home/pedro-kraken/Área\ de\ trabalho/SISCAP
git remote add origin https://github.com/seu-usuario/SISCAP.git
git branch -M main
git push -u origin main
```

#### Opção B: SSH (recomendado)
```bash
# Primeiro, configure SSH (execute uma única vez)
ssh-keygen -t ed25519 -C "seu-email@example.com"
# Copie a chave pública para github.com/settings/keys

# Depois:
cd /home/pedro-kraken/Área\ de\ trabalho/SISCAP
git remote add origin git@github.com:seu-usuario/SISCAP.git
git branch -M main
git push -u origin main
```

### 4️⃣ Verifique o Push

```bash
# Ver repositórios remotos
git remote -v

# Ver branches remotos
git branch -r
```

---

## 📚 Comandos Úteis

### Ver Informações
```bash
git status              # Status atual
git log --oneline       # Histórico resumido
git log --all --graph   # Gráfico de commits
git remote -v           # Repositórios remotos
```

### Fazer Alterações (após editar arquivos)
```bash
git add .               # Preparar mudanças
git commit -m "msg"     # Fazer commit local
git push                # Subir para repositório remoto
```

### Atualizar Código
```bash
git pull                # Baixar e mesclar alterações
git fetch               # Apenas baixar (sem mesclar)
```

---

## ⚠️ Verificação do .gitignore

Arquivos **excluídos** do versionamento (correto):
- ✗ `siscap.db` (banco de dados)
- ✗ `.venv/` (ambiente virtual)
- ✗ `__pycache__/` (cache Python)
- ✗ `.pytest_cache/` (cache de testes)

Arquivos **inclusos** do versionamento (correto):
- ✓ Código-fonte (`.py`)
- ✓ Documentação (`.md`, `.txt`)
- ✓ Configuração (`.gitignore`)

---

## 🔐 Segurança

⚠️ **Nunca** faça push de:
- Chaves API ou tokens
- Senhas ou credenciais
- Dados sensíveis

Se acidentalmente fizer push, use:
```bash
git rm --cached arquivo.txt
git commit -m "Remove sensitive file"
git push
```

---

## 📝 Dicas de Commit

Use mensagens claras e descritivas:

```bash
# BOM ✓
git commit -m "feat: Add ABC validation for Pessoa class"
git commit -m "fix: Correct SQL query in gerenciador_bd"
git commit -m "docs: Update README with execution instructions"

# RUIM ✗
git commit -m "changes"
git commit -m "fix"
git commit -m "aaa"
```

---

## 🎯 Fluxo Típico de Trabalho

1. **Faça alterações** no código
2. **Teste localmente**: `python -m siscap.main`
3. **Prepare**: `git add .`
4. **Commit local**: `git commit -m "sua mensagem"`
5. **Push remoto**: `git push`

---

## 📞 Suporte

Se encontrar problemas:

```bash
# Verificar configuração
git config --list

# Reset se necessário
git reset HEAD arquivo.txt

# Ver diferenças
git diff
git diff --cached
```

---

**✨ Seu projeto está pronto para controle de versão!**

Qualquer dúvida sobre Git, consulte: https://git-scm.com/doc
