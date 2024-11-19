import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import tkinter as tk
from tkinter import messagebox, filedialog, Toplevel

# Nachricht und Anhänge konfigurieren
def sende_email(empfaenger, anhaenge_pfade=None, absender_email=None, absender_passwort=None, nachricht_text=None, betreff=None):
    try:
        # Nachricht erstellen
        msg = MIMEMultipart()
        msg['From'] = absender_email
        msg['To'] = ", ".join(empfaenger)  # Empfänger werden als durch Kommas getrennte Liste gesetzt
        msg['Subject'] = betreff  # Benutzerdefinierter Betreff

        # Nachrichtentext
        msg.attach(MIMEText(nachricht_text, 'plain'))

        # Anhänge hinzufügen, falls vorhanden
        if anhaenge_pfade:
            for anhang_pfad in anhaenge_pfade:
                if os.path.exists(anhang_pfad):  # Prüfe, ob die Datei existiert
                    with open(anhang_pfad, 'rb') as anhang_datei:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(anhang_datei.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename="{os.path.basename(anhang_pfad)}"'
                        )
                        msg.attach(part)
                else:
                    print(f"Anhang nicht gefunden: {anhang_pfad}")

        # Verbindung zum SMTP-Server herstellen
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(absender_email, absender_passwort)
            server.sendmail(absender_email, empfaenger, msg.as_string())

        print(f"E-Mail erfolgreich an {', '.join(empfaenger)} gesendet.")
    except Exception as e:
        print(f"Fehler beim Senden an {', '.join(empfaenger)}: {e}")

# Anleitung für das App-Passwort anzeigen
def app_passwort_anleitung():
    anleitung_fenster = Toplevel()
    anleitung_fenster.title("Anleitung: App-Passwort erstellen")

    anleitung_text = """
    Um ein App-Passwort für deinen Google-Account zu erstellen, folge diesen Schritten:

    1. Melde dich bei deinem Google-Konto an: Gehe auf https://myaccount.google.com/ und melde dich mit deinem Google-Konto an.

    2. Gehe zu den Sicherheits-Einstellungen:
       - Klicke auf "Sicherheit" im linken Menü.

    3. App-Passwörter erstellen:
       - Unter dem Abschnitt "Anmeldung bei Google" solltest du die Option "App-Passwörter" sehen.
       - Klicke darauf. Falls du diese Option nicht siehst, könnte es daran liegen, dass du die Zwei-Faktor-Authentifizierung (2FA) nicht aktiviert hast. Falls das der Fall ist, musst du 2FA einrichten, bevor du ein App-Passwort generieren kannst.

    4. App-Passwort erstellen:
       - Wenn die Zwei-Faktor-Authentifizierung aktiviert ist, kannst du ein App-Passwort erstellen.
       - Wähle aus der Dropdown-Liste die App und das Gerät aus, für das du das Passwort erstellen möchtest. Wenn deine App nicht in der Liste erscheint, wähle "Andere (benutzerdefiniert)" und gib einen Namen ein, z. B. "E-Mail-App".
       - Klicke auf "Generieren".

    5. Passwort kopieren und verwenden:
       - Google zeigt dir nun ein 16-stelliges App-Passwort. Kopiere dieses Passwort und verwende es in der entsprechenden App, anstelle deines regulären Google-Kennworts.
    """
    label_anleitung = tk.Label(anleitung_fenster, text=anleitung_text, justify=tk.LEFT, padx=10, pady=10)
    label_anleitung.pack()

    # Schließen Button
    button_schliessen = tk.Button(anleitung_fenster, text="Schließen", command=anleitung_fenster.destroy)
    button_schliessen.pack(pady=10)

# GUI erstellen
def sende_email_gui():
    def on_send():
        absender_email = entry_email.get()
        absender_passwort = entry_passwort.get()
        nachricht_text = text_nachricht.get("1.0", tk.END).strip()  # Strip entfernt Leerzeichen und Zeilenumbrüche
        betreff = entry_betreff.get().strip()  # Betreff wird aus dem Eingabefeld entnommen
        empfaenger_emails = entry_empfaenger.get().split(",")  # Empfänger durch Kommas getrennt eingeben

        # Entfernen von führenden/trailing Leerzeichen aus den Empfänger-E-Mails
        empfaenger_emails = [email.strip() for email in empfaenger_emails]

        # Validierung
        if not absender_email or not absender_passwort:
            messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
            return
        
        if not nachricht_text:
            messagebox.showerror("Fehler", "Bitte verfassen Sie eine Nachricht.")
            return

        if not betreff:
            messagebox.showerror("Fehler", "Bitte geben Sie einen Betreff ein.")
            return

        if not empfaenger_emails:
            messagebox.showerror("Fehler", "Bitte geben Sie mindestens eine Empfänger-E-Mail-Adresse ein.")
            return

        # E-Mails senden
        sende_email(empfaenger_emails, anhaenge if anhaenge else None, absender_email, absender_passwort, nachricht_text, betreff)

        messagebox.showinfo("Erfolg", "E-Mails wurden erfolgreich gesendet!")

    def add_anhaenge():
        # Dateien auswählen (unterstützt mehrere Dateitypen)
        anhaenge_dateien = filedialog.askopenfilenames(
            title="Wählen Sie die Anhänge aus",
            filetypes=(
                ("Alle unterstützten Dateien", "*.pdf;*.mp3;*.jpg;*.png;*.*"),
                ("PDF-Dateien", "*.pdf"),
                ("MP3-Dateien", "*.mp3"),
                ("JPG-Dateien", "*.jpg"),
                ("PNG-Dateien", "*.png"),
                ("Alle Dateien", "*.*")
            )
        )
        
        # Liste der Anhänge aktualisieren
        if anhaenge_dateien:
            anhaenge.clear()
            anhaenge.extend(anhaenge_dateien)
            label_anhaenge.config(text=f"Angehängte Dateien: {len(anhaenge)}")

    # Fenster erstellen
    window = tk.Tk()
    window.title("E-Mail Sender")

    # Eingabefelder
    tk.Label(window, text="Ihre E-Mail-Adresse:").pack(padx=10, pady=5)
    entry_email = tk.Entry(window, width=50)
    entry_email.pack(padx=10, pady=5)

    tk.Label(window, text="Ihr Passwort:").pack(padx=10, pady=5)
    entry_passwort = tk.Entry(window, width=50, show="*")
    entry_passwort.pack(padx=10, pady=5)

    tk.Label(window, text="Empfänger E-Mail-Adressen (durch Komma getrennt):").pack(padx=10, pady=5)
    entry_empfaenger = tk.Entry(window, width=50)
    entry_empfaenger.pack(padx=10, pady=5)

    tk.Label(window, text="Betreff der E-Mail:").pack(padx=10, pady=5)
    entry_betreff = tk.Entry(window, width=50)
    entry_betreff.pack(padx=10, pady=5)

    tk.Label(window, text="Nachricht:").pack(padx=10, pady=5)
    text_nachricht = tk.Text(window, height=10, width=50)
    text_nachricht.pack(padx=10, pady=5)

    # Button zum Hinzufügen von Anhängen
    anhaenge = []  # Liste zum Speichern der Anhänge
    button_anhaenge = tk.Button(window, text="Anhänge hinzufügen", command=add_anhaenge)
    button_anhaenge.pack(padx=10, pady=5)

    # Label, um die Anzahl der Anhänge anzuzeigen
    label_anhaenge = tk.Label(window, text="Angehängte Dateien: 0")
    label_anhaenge.pack(padx=10, pady=5)

    # Button für die Anleitung zum App-Passwort
    button_anleitung = tk.Button(window, text="Anleitung zum App-Passwort", command=app_passwort_anleitung)
    button_anleitung.pack(padx=10, pady=5)

    # Senden Button
    send_button = tk.Button(window, text="E-Mails senden", command=on_send)
    send_button.pack(padx=10, pady=10)

    window.mainloop()

# Hauptprogramm
if __name__ == "__main__":
    sende_email_gui()









