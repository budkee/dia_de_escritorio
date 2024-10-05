import os
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv  # Importa a biblioteca dotenv


class EmailScheduler:
    def __init__(self, sender_email, receiver_email, password):
        self.sender_email = sender_email
        self.receiver_email = receiver_email
        self.password = password

    def send_email(self):
        subject = "Semana de atualização da planilha financeira"
        body = "Este é um lembrete de que é semana de atualização da planilha financeira."

        # Cria a mensagem de e-mail
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = self.receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            # Configuração do servidor SMTP
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Segurança
            server.login(self.sender_email, self.password)

            # Envia o e-mail
            server.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            print("E-mail enviado com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")
        finally:
            server.quit()

    def job(self):
        # Verifica se estamos na primeira semana do mês
        today = datetime.today()
        if today.day <= 7:  # Apenas executa na primeira semana
            print("Enviando notificação por email.")
            self.send_email()
        else:
            print("Fora da primeira semana do mês. Nenhuma ação tomada.")

    def schedule_job(self):
        # Executa o job imediatamente
        self.job()
        
        # Agendar o job para ser executado na próxima execução desejada
        schedule.every().saturday.at("09:00").do(self.job)

    def run(self):
        # Loop para executar o agendamento
        while True:
            schedule.run_pending()
            time.sleep(60)  # Verifica a cada minuto


if __name__ == "__main__":
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()

    # Obtém as variáveis de ambiente
    sender_email = os.environ.get("GMAIL_USER")
    receiver_email = "kae.budke@ufms.br"
    password = os.getenv("GMAIL_PASS")

    # Cria uma instância da classe EmailScheduler e inicia o agendamento
    email_scheduler = EmailScheduler(sender_email, receiver_email, password)
    email_scheduler.schedule_job()
    email_scheduler.run()
