import customtkinter as ctk
from datetime import datetime, timedelta
from tkinter import messagebox

# Configuração de Aparência
ctk.set_appearance_mode("light") 

class AppBarbearia(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Agendamento Gold & White")
        self.geometry("600x500")
        self.configure(fg_color="#FFFFFF") # Fundo Branco

        # Cores do Tema
        self.gold = "#D4AF37"
        self.black = "#1A1A1A"
        self.white = "#FFFFFF"

        # Banco de dados temporário (em memória)
        self.agendamentos = []

        self.setup_ui()

    def setup_ui(self):
        # Título
        self.lbl_titulo = ctk.CTkLabel(self, text="BARBEARIA PREMIUM", 
                                       font=("Helvetica", 24, "bold"), 
                                       text_color=self.black)
        self.lbl_titulo.pack(pady=20)

        # Frame Central
        self.frame = ctk.CTkFrame(self, fg_color=self.white, border_color=self.gold, border_width=2)
        self.frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Inputs
        self.label_nome = ctk.CTkLabel(self.frame, text="Nome do Cliente:", text_color=self.black)
        self.label_nome.pack(pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self.frame, width=300, fg_color=self.white, border_color=self.gold, text_color=self.black)
        self.entry_nome.pack(pady=5)

        self.label_data = ctk.CTkLabel(self.frame, text="Data e Hora (Ex: 24/02 14:00):", text_color=self.black)
        self.label_data.pack(pady=(10, 0))
        self.entry_data = ctk.CTkEntry(self.frame, width=300, fg_color=self.white, border_color=self.gold, text_color=self.black)
        self.entry_data.pack(pady=5)

        # Botão Agendar
        self.btn_agendar = ctk.CTkButton(self.frame, text="Confirmar Agendamento", 
                                         fg_color=self.gold, hover_color="#B89B2E",
                                         text_color=self.black, font=("Helvetica", 14, "bold"),
                                         command=self.adicionar_agendamento)
        self.btn_agendar.pack(pady=20)

        # Lista de Agendamentos
        self.label_lista = ctk.CTkLabel(self.frame, text="Próximos Horários (Duração 45min):", text_color=self.black, font=("Helvetica", 12, "italic"))
        self.label_lista.pack()
        
        self.txt_lista = ctk.CTkTextbox(self.frame, width=450, height=150, fg_color="#F9F9F9", border_color=self.gold, text_color=self.black)
        self.txt_lista.pack(pady=10)

    def adicionar_agendamento(self):
        nome = self.entry_nome.get()
        data_str = self.entry_data.get()

        if not nome or not data_str:
            messagebox.showwarning("Erro", "Preencha todos os campos!")
            return

        try:
            # Tenta converter a data (ajuste o ano conforme necessário)
            data_inicio = datetime.strptime(f"{data_str}/2026", "%d/%m/%Y %H:%M")
            data_fim = data_inicio + timedelta(minutes=45)

            # Verifica conflito de horário
            for ag in self.agendamentos:
                if (data_inicio < ag['fim']) and (data_fim > ag['inicio']):
                    messagebox.showerror("Conflito", "Este horário já está ocupado!")
                    return

            # Adiciona à lista
            agendamento = {"nome": nome, "inicio": data_inicio, "fim": data_fim}
            self.agendamentos.append(agendamento)
            self.agendamentos.sort(key=lambda x: x['inicio']) # Organiza por hora

            self.atualizar_lista()
            self.entry_nome.delete(0, 'end')
            self.entry_data.delete(0, 'end')
            messagebox.showinfo("Sucesso", f"Agendado: {nome}\nAté as {data_fim.strftime('%H:%M')}")

        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use: DD/MM HH:MM")

    def atualizar_lista(self):
        self.txt_lista.delete("1.0", "end")
        for ag in self.agendamentos:
            linha = f"{ag['inicio'].strftime('%d/%m %H:%M')} - {ag['nome']} (Fim: {ag['fim'].strftime('%H:%M')})\n"
            self.txt_lista.insert("end", linha)

if __name__ == "__main__":
    app = AppBarbearia()
    app.mainloop()
