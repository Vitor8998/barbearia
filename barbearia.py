import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import urllib.parse
import webbrowser
import json
import os

# Configuração base do tema
ctk.set_appearance_mode("light")

class AppBarbearia(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Golden Cut - Sistema de Agendamento")
        self.geometry("1000x650")
        self.configure(fg_color="#FFFFFF") # Fundo Branco

        # Paleta de Cores
        self.color_gold = "#D4AF37"
        self.color_black = "#1A1A1A"
        self.color_white = "#FFFFFF"
        
        self.agendamentos = self.carregar_dados()

        self.setup_ui()

    def setup_ui(self):
        # --- Painel Lateral (Formulário) ---
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=0, fg_color=self.color_white, border_width=2, border_color=self.color_gold)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="GOLDEN CUT", font=ctk.CTkFont(size=28, weight="bold"), text_color=self.color_gold)
        self.logo_label.pack(pady=(30, 20))

        # Campos
        self.criar_campo("Nome do Cliente:", "entry_nome")
        self.criar_campo("Telefone (com DDD):", "entry_telefone", placeholder="Ex: 11999999999")
        self.criar_campo("Data (DD/MM/AAAA):", "entry_data", valor_padrao=datetime.now().strftime("%d/%m/%Y"))
        self.criar_campo("Horário (HH:MM):", "entry_hora", placeholder="Ex: 14:30")

        self.btn_agendar = ctk.CTkButton(self.sidebar, text="AGENDAR (45 MIN)", fg_color=self.color_gold, 
                                        text_color=self.color_black, hover_color="#B8860B", 
                                        font=ctk.CTkFont(weight="bold", size=14),
                                        command=self.adicionar_agendamento)
        self.btn_agendar.pack(fill="x", padx=20, pady=25)

        # --- Área Principal (Tabela) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.title_list = ctk.CTkLabel(self.main_frame, text="Próximos Atendimentos", 
                                      font=ctk.CTkFont(size=22, weight="bold"), text_color=self.color_black)
        self.title_list.pack(pady=(10, 20))

        # Configuração da Tabela
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'), background=self.color_gold, foreground=self.color_black)
        style.configure("Treeview", background=self.color_white, fieldbackground=self.color_white, foreground=self.color_black, rowheight=35)
        style.map("Treeview", background=[('selected', '#F0E6D2')]) # Dourado claro ao selecionar

        self.tree = ttk.Treeview(self.main_frame, columns=("Cliente", "Telefone", "Data", "Início", "Fim"), show='headings')
        self.tree.heading("Cliente", text="CLIENTE")
        self.tree.heading("Telefone", text="TELEFONE")
        self.tree.heading("Data", text="DATA")
        self.tree.heading("Início", text="INÍCIO")
        self.tree.heading("Fim", text="FIM")
        
        self.tree.column("Telefone", width=120)
        self.tree.column("Data", width=100)
        self.tree.column("Início", width=80)
        self.tree.column("Fim", width=80)
        self.tree.pack(fill="both", expand=True)

        # Botão de WhatsApp
        self.btn_wpp = ctk.CTkButton(self.main_frame, text="ENVIAR LEMBRETE VIA WHATSAPP", 
                                     fg_color=self.color_black, text_color=self.color_gold, 
                                     hover_color="#333333", font=ctk.CTkFont(weight="bold"),
                                     command=self.enviar_whatsapp)
        self.btn_wpp.pack(pady=20, fill="x")
        
        self.atualizar_tabela()

    def criar_campo(self, texto_label, nome_atributo, valor_padrao="", placeholder=""):
        label = ctk.CTkLabel(self.sidebar, text=texto_label, text_color=self.color_black, font=ctk.CTkFont(weight="bold"))
        label.pack(padx=20, anchor="w", pady=(10, 0))
        entry = ctk.CTkEntry(self.sidebar, fg_color=self.color_white, text_color=self.color_black, border_color=self.color_gold, placeholder_text=placeholder)
        if valor_padrao:
            entry.insert(0, valor_padrao)
        entry.pack(fill="x", padx=20, pady=(2, 0))
        setattr(self, nome_atributo, entry)

    def adicionar_agendamento(self):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        data_str = self.entry_data.get().strip()
        hora_str = self.entry_hora.get().strip()

        if not nome or not telefone or not data_str or not hora_str:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        try:
            inicio = datetime.strptime(f"{data_str} {hora_str}", "%d/%m/%Y %H:%M")
            fim = inicio + timedelta(minutes=45)
            
            # Evita chocar horários
            for ag in self.agendamentos:
                ag_inicio = datetime.strptime(f"{ag['data']} {ag['inicio']}", "%d/%m/%Y %H:%M")
                ag_fim = datetime.strptime(f"{ag['data']} {ag['fim']}", "%d/%m/%Y %H:%M")
                
                if (inicio < ag_fim and fim > ag_inicio):
                    messagebox.showerror("Erro", "Horário indisponível! Conflito com outro cliente.")
                    return

            novo_ag = {"cliente": nome, "telefone": telefone, "data": data_str, "inicio": hora_str, "fim": fim.strftime("%H:%M")}
            self.agendamentos.append(novo_ag)
            self.salvar_dados()
            self.atualizar_tabela()
            
            self.entry_nome.delete(0, 'end')
            self.entry_telefone.delete(0, 'end')
            self.entry_hora.delete(0, 'end')
            messagebox.showinfo("Sucesso", f"Atendimento de {nome} marcado com sucesso!")

        except ValueError:
            messagebox.showerror("Erro", "Formato de data (DD/MM/AAAA) ou hora (HH:MM) inválido!")

    def atualizar_tabela(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.agendamentos.sort(key=lambda x: datetime.strptime(f"{x['data']} {x['inicio']}", "%d/%m/%Y %H:%M"))
        for ag in self.agendamentos:
            self.tree.insert("", "end", values=(ag['cliente'], ag['telefone'], ag['data'], ag['inicio'], ag['fim']))

    def enviar_whatsapp(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente na tabela primeiro.")
            return
        
        valores = self.tree.item(selecionado[0], "values")
        nome, telefone, data, inicio = valores[0], valores[1], valores[2], valores[3]
        
        telefone_formatado = ''.join(filter(str.isdigit, telefone))
        mensagem = f"Olá {nome}! Passando para confirmar seu horário na Golden Cut amanhã, {data} às {inicio}. Te aguardamos!"
        mensagem_url = urllib.parse.quote(mensagem)
        
        link = f"https://api.whatsapp.com/send?phone=55{telefone_formatado}&text={mensagem_url}"
        webbrowser.open(link)

    def salvar_dados(self):
        with open("agenda_barbearia.json", "w", encoding="utf-8") as f:
            json.dump(self.agendamentos, f, ensure_ascii=False, indent=4)

    def carregar_dados(self):
        if os.path.exists("agenda_barbearia.json"):
            with open("agenda_barbearia.json", "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    app = AppBarbearia()
    app.mainloop()
