import sys
from PySide6.QtWidgets import *
import sqlite3

class FormularioOficina(QMainWindow):
    def __init__(self):
        super(FormularioOficina, self).__init__()

        # Conectar ao banco de dados SQLite
        self.conexao = sqlite3.connect('oficina.db')
        # Criar a tabela 'clientes' se ela ainda não existir
        self.criar_tabela_cliente()

        # Configurações básicas da janela principal
        self.setWindowTitle("Formulário Oficina")
        self.setGeometry(100, 100, 600, 400)

        # Configurar o layout da interface gráfica
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()

        # Widgets para entrada de dados e botões
        self.label_nome = QLabel("Nome do cliente:")
        self.edit_nome = QLineEdit()

        self.label_servico = QLabel("Serviço:")
        self.edit_servico = QLineEdit()

        self.label_peca = QLabel("Valor da peça:")
        self.edit_peca = QLineEdit()

        self.label_obra = QLabel("Mão de obra:")
        self.edit_obra = QLineEdit()

        self.btn_adicionar = QPushButton("Adicionar")
        self.btn_adicionar.clicked.connect(self.adicionar_cliente)

        self.btn_deletar = QPushButton("Deletar Selecionado")
        self.btn_deletar.clicked.connect(self.deletar_cliente)

        self.btn_mostrar = QPushButton("Mostrar Tabela")
        self.btn_mostrar.clicked.connect(self.mostrar_tabela)

        self.btn_atualizar = QPushButton("Atualizar Selecionado")
        self.btn_atualizar.clicked.connect(self.atualizar_cliente)

        # Tabela para mostrar os dados
        self.table_widget = QTableWidget()

        # Adicionar widgets ao layout
        self.layout.addWidget(self.label_nome)
        self.layout.addWidget(self.edit_nome)
        self.layout.addWidget(self.label_servico)
        self.layout.addWidget(self.edit_servico)
        self.layout.addWidget(self.label_peca)
        self.layout.addWidget(self.edit_peca)
        self.layout.addWidget(self.label_obra)
        self.layout.addWidget(self.edit_obra)
        self.layout.addWidget(self.btn_adicionar)
        self.layout.addWidget(self.btn_deletar)
        self.layout.addWidget(self.btn_atualizar)
        self.layout.addWidget(self.btn_mostrar)
        self.layout.addWidget(self.table_widget)

        self.central_widget.setLayout(self.layout)

    def criar_tabela_cliente(self):
        # Criar a tabela 'clientes' se ela não existir
        cursor = self.conexao.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                servico TEXT,
                peca REAL,
                obra REAL,
                total REAL
            )
        ''')
        self.conexao.commit()

    def adicionar_cliente(self):
        # Obter dados do cliente a partir dos campos de entrada
        nome = self.edit_nome.text()
        servico = self.edit_servico.text()
        peca = float(self.edit_peca.text())
        obra = float(self.edit_obra.text())
        total = peca + obra

        # Inserir os dados do cliente no banco de dados
        cursor = self.conexao.cursor()
        cursor.execute('''
            INSERT INTO clientes (nome, servico, peca, obra, total)
            VALUES (?, ?, ?, ?, ?)
        ''', (nome, servico, peca, obra, total))

        # Limpar os campos de entrada
        self.edit_nome.clear()
        self.edit_servico.clear()
        self.edit_peca.clear()
        self.edit_obra.clear()

        # Commit para salvar as alterações no banco de dados
        self.conexao.commit()
        # Atualizar a tabela na interface gráfica
        self.mostrar_tabela()

    def deletar_cliente(self):
        # Verificar se uma linha da tabela está selecionada
        if self.table_widget.currentRow() >= 0:
            selected_row = self.table_widget.currentRow()
            cursor = self.conexao.cursor()
            # Obter o ID do cliente na linha selecionada
            cliente_id = self.table_widget.item(selected_row, 0).text()
            # Excluir o cliente do banco de dados
            cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
            # Commit para salvar as alterações no banco de dados
            self.conexao.commit()
            # Atualizar a tabela na interface gráfica
            self.mostrar_tabela()

    def atualizar_cliente(self):
        if self.table_widget.currentRow() >= 0:
            selected_row = self.table_widget.currentRow()
            cursor = self.conexao.cursor()
             # Obter o ID do cliente na linha selecionada
            cliente_id = self.table_widget.item(selected_row, 0).text()
             # Consultar os dados do cliente com base no ID
            cursor.execute('SELECT * FROM clientes WHERE id = ?', (cliente_id,))
            cliente = cursor.fetchone()

            # Preencher os campos de edição com os dados existentes
            self.edit_nome.setText(cliente[1])
            self.edit_servico.setText(cliente[2])
            self.edit_peca.setText(str(cliente[3]))
            self.edit_obra.setText(str(cliente[4]))

            # Deletar o cliente existente (opcional, dependendo dos requisitos)
            cursor.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
            # Atualizar a tabela para refletir as mudanças
            self.mostrar_tabela()

    def mostrar_tabela(self):
        # Consultar todos os clientes no banco de dados
        cursor = self.conexao.cursor()
        cursor.execute('SELECT * FROM clientes')
        clientes = cursor.fetchall()

        # Configurar a tabela na interface gráfica
        self.table_widget.setRowCount(len(clientes))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Nome", "Serviço", "Peças", "M-Obra", "Total"])

        # Preencher a tabela com os dados dos clientes
        for row, cliente in enumerate(clientes):
            for col, value in enumerate(cliente):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

if __name__ == "__main__":
    # Iniciar a aplicação
    app = QApplication(sys.argv)
    formulario_app = FormularioOficina()
    formulario_app.show()
    sys.exit(app.exec_())
