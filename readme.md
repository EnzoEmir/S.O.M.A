
# Assistente Pessoal

Um assistente pessoal minimalista, feito em Python com PySide6, para organização da rotina diária.  
---

## Funcionalidades

### **Agenda Inteligente**
- Calendário visual com 4 tipos de tarefas: único(Importante), diário e semanal
- Eventos importantes com destaque especial
- Sistema de cores e filtros por tipo

### **Acompanhamento de Progresso**
- Check-off de tarefas com cálculo automático de conclusão
- Barras de progresso visuais e streak de dias perfeitos
- Notificações de parabenização

### **Histórico e Estatísticas**
- Relatórios detalhados por período
- Taxa de conclusão e trends de produtividade
- Contagem regressiva para eventos importantes



---

## Tecnologias utilizadas

- [Python 3.10+](https://www.python.org/)
- [PySide6 (Qt for Python)](https://doc.qt.io/qtforpython/)
- **JSON** - Armazenamento local de dados

---

## 🗂 Estrutura do Projeto


```
S.O.M.A/
├── main.py                    # Ponto de entrada da aplicação
├── criar_atalho.bat          # Script para criar atalho na área de trabalho
├── main.ico                  # Ícone da aplicação
├── requirements.txt          # Dependências Python
│
├── SOMA/                     # Módulo principal
│   ├── minhas_datas.json    # Banco de dados local
│   │
│   ├── inicial/             # Tela principal e menu
│   │   ├── ui.py           # Interface do menu principal
│   │   └── controller.py   # Lógica de navegação
│   │
│   ├── agenda/             # Sistema de agenda
│   │   ├── agenda_ui.py           # Interface principal da agenda
│   │   ├── agenda_controller.py   # Controlador de tarefas
│   │   ├── adicionar_tarefa_ui.py # Formulário de nova tarefa
│   │   ├── tarefas_do_dia_ui.py   # Visualização diária
│   │   ├── calendario_customizado.py # Calendário com barras visuais
│   │   └── delecao.py             # Sistema de remoção
│   │
│   ├── atividades/         # Gerenciamento de atividades
│   │   ├── atividades_ui.py       # Interface principal
│   │   ├── atividades_controller.py # Lógica de progresso
│   │   └── historico_ui.py        # Relatórios e estatísticas
│   │
│   └── navegacao/          # Sistema de navegação
│       └── stack.py        # Stack de páginas e histórico
```

---

## Motivação

A ideia nasceu da necessidade de um assistente **simples e offline** para:

- Organizar tarefas do dia a dia
- Manter lembretes visíveis
- Visualizar rapidamente o que está pendente

O projeto também serve como estudo prático de GUI com **PySide6**, e como **exemplo** para portfólio.

---

## Como executar

1. Clone este repositório:

```bash
git clone https://github.com/EnzoEmir/S.O.M.A.git
cd SOMA
```

2. (Opcional) Crie e ative um ambiente virtual:

```bash
python -m venv .venv
# Ative no Linux/macOS:
source .venv/bin/activate
# Ou no Windows:
.venv\Scripts\activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Execute a aplicação:

```bash
python main.py
```

5. Caso deseje um atalho na area de trabalho (somente Windows) :

```bash
.\criar_atalho.bat
```

---

## Contato

Feito por **Enzo Emir** – contribuições, ideias e sugestões são bem-vindas!

**GitHub**: [@EnzoEmir](https://github.com/EnzoEmir)
