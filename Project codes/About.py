import tkinter as tk
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Sample data for demonstration (pretend this is the prevalence of each attack type)
attack_prevalence = {
    "Phishing": 20,
    "Malware": 15,
    "DoS Attack": 10,
    "MitM Attack": 5,
    "SQL Injection": 8,
    "XSS": 7,
    "Credential Stuffing": 3,
    "Brute Force": 6,
    "DNS Spoofing": 2,
    "Session Hijacking": 4
}

# Attack descriptions with additional information
attack_descriptions = {
    "Phishing": {
        "Title": "Phishing",
        "Mechanism": "Attackers impersonate legitimate entities to trick individuals into revealing sensitive information through deceptive emails, messages, or websites.",
        "Types": "Email phishing, spear phishing, pharming, whaling, vishing, smishing.",
        "Rank from attacking": "Common and highly effective.",
        "Safety/Prevention": "Be cautious of suspicious emails or messages, verify website authenticity, use two-factor authentication, educate users about phishing techniques.",
        "Consequences": "Unauthorized access to personal information, financial loss, identity theft.",
        "Link": "https://www.kaspersky.com/resource-center/definitions/what-is-phishing"
    },
    "Malware": {
        "Title": "Malware",
        "Mechanism": "Malicious software designed to harm or exploit computer systems.",
        "Types": "Viruses, worms, Trojans, ransomware, spyware.",
        "Rank from attacking": "Common and highly damaging.",
        "Safety/Prevention": "Use reputable antivirus software, keep systems and software up to date, exercise caution when downloading files or clicking on links, regularly backup data.",
        "Consequences": "Data loss, system disruption, unauthorized access, financial loss.",
        "Link": "https://us.norton.com/internetsecurity-malware-what-is-malware.html"
    },
    "DoS Attack": {
        "Title": "DoS Attack (Denial of Service)",
        "Mechanism": "Overwhelming a system or network with illegitimate requests or traffic to disrupt availability.",
        "Types": "SYN flood, UDP flood, ICMP flood, HTTP flood.",
        "Rank from attacking": "Common and disruptive.",
        "Safety/Prevention": "Implement network traffic monitoring, use firewalls and load balancers, employ rate limiting and traffic filtering techniques.",
        "Consequences": "Service disruptions, loss of revenue, reputational damage.",
        "Link": "https://www.cloudflare.com/learning/ddos/what-is-a-dos-attack/"
    },
    "MitM Attack": {
        "Title": "MitM Attack (Man-in-the-Middle)",
        "Mechanism": "Intercepting and altering communication between two parties without their knowledge.",
        "Types": "IP spoofing, ARP spoofing, SSL stripping.",
        "Rank from attacking": "Sophisticated and dangerous.",
        "Safety/Prevention": "Use secure communication protocols (e.g., HTTPS), implement certificate validation, utilize VPNs, be cautious of unsecured networks.",
        "Consequences": "Data interception, unauthorized access, information tampering.",
        "Link": "https://www.imperva.com/learn/application-security/man-in-the-middle-attack-mitm/"
    },
    "SQL Injection": {
        "Title": "SQL Injection",
        "Mechanism": "Exploiting web application vulnerabilities to manipulate SQL queries and gain unauthorized access to databases.",
        "Types": "Classic SQL injection, blind SQL injection, time-based blind SQL injection.",
        "Rank from attacking": "Common and damaging.",
        "Safety/Prevention": "Implement input validation and parameterized queries, apply least privilege principle, regularly update and patch applications.",
        "Consequences": "Unauthorized data access, data manipulation, data loss.",
        "Link": "https://owasp.org/www-community/attacks/SQL_Injection"
    },
    "XSS": {
        "Title": "XSS (Cross-Site Scripting)",
        "Mechanism": "Injecting malicious scripts into web pages viewed by other users.",
        "Types": "Stored XSS, reflected XSS, DOM-based XSS.",
        "Rank from attacking": "Common and impactful.",
        "Safety/Prevention": "Implement input sanitization, encode user-generated content, use Content Security Policy (CSP), educate developers about secure coding practices.",
        "Consequences": "Data theft, session hijacking, defacement of websites.",
        "Link": "https://portswigger.net/web-security/cross-site-scripting"
    },
    "Credential Stuffing": {
        "Title": "Credential Stuffing",
        "Mechanism": "Using stolen credentials from one website to gain unauthorized access to user accounts on other websites.",
        "Types": "Automated credential stuffing, manual credential stuffing.",
        "Rank from attacking": "Common and effective against reused credentials.",
        "Safety/Prevention": "Encourage unique passwords, implement multi-factor authentication, monitor for suspicious login attempts, educate users about password hygiene.",
        "Consequences": "Account takeover, identity theft, unauthorized access to personal information.",
        "Link": "https://www.imperva.com/learn/application-security/credential-stuffing/"
    },
    "Brute Force": {
        "Title": "Brute Force",
        "Mechanism": "Trying all possible combinations of passwords or encryption keys until the correct one is found.",
        "Types": "Online brute force, offline brute force.",
        "Rank from attacking": "Common but time-consuming.",
        "Safety/Prevention": "Enforce strong password policies, implement account lockouts and rate limiting, use CAPTCHA or other anti-automation measures.",
        "Consequences": "Unauthorized access, data theft, system compromise.",
        "Link": "https://www.cloudflare.com/learning/ddos/brute-force-attack/"
    },
    "DNS Spoofing": {
        "Title": "DNS Spoofing",
        "Mechanism": "Manipulating the Domain Name System (DNS) to redirect users to malicious websites or intercept their communications.",
        "Types": "Cache poisoning, DNS hijacking.",
        "Rank from attacking": "Less common but impactful.",
        "Safety/Prevention": "Implement DNSSEC, regularly update DNS software, use DNS filtering services, monitor DNS traffic for anomalies.",
        "Consequences": "Phishing attacks, data interception, unauthorized website redirection.",
        "Link": "https://www.cloudflare.com/learning/dns/dns-spoofing/"
    },
    "Session Hijacking": {
        "Title": "Session Hijacking",
        "Mechanism": "Intercepting and taking control of a user's active session on a website or web application.",
        "Types": "Session sidejacking, session fixation.",
        "Rank from attacking": "Less common but dangerous.",
        "Safety/Prevention": "Use secure session management techniques, employ secure cookies, implement session expiration and reauthentication mechanisms.",
        "Consequences": "Unauthorized access to user accounts, data exposure, impersonation.",
        "Link": "https://owasp.org/www-community/attacks/Session_hijacking_attack"
    }
}

# Create the main application window
app = tk.Tk()
app.title("Cyber Attack Encyclopedia")
app.configure(bg='skyblue')  # Set application background color

# Function to display attack description and plot pie chart
def show_attack_details(event):
    selected_attack = listbox_attacks.get(listbox_attacks.curselection())
    attack_info = attack_descriptions[selected_attack]
    description = f"Title: {attack_info['Title']}\n\nMechanism: {attack_info['Mechanism']}\n\nTypes: {attack_info['Types']}\n\nRank from attacking: {attack_info['Rank from attacking']}\n\nSafety/Prevention: {attack_info['Safety/Prevention']}\n\nConsequences: {attack_info['Consequences']}"
    text_description.config(state=tk.NORMAL, bg='black', fg='skyblue', font=("Courier", 12))  # Set text color to skyblue and background color to black, increase font size
    text_description.delete('1.0', tk.END)
    typewriter_effect(description)

# Function to simulate typing effect
def typewriter_effect(description):
    for char in description:
        text_description.insert(tk.END, char)
        text_description.update()
        time.sleep(0.03)  # Adjust typing speed here
    text_description.config(state=tk.DISABLED)

# List of Attacks
frame_attacks = tk.LabelFrame(app, text="List of Cyber Attacks", bg='black', fg='red')
frame_attacks.grid(row=0, column=0, padx=10, pady=10, sticky=tk.N+tk.S)

listbox_attacks = tk.Listbox(frame_attacks, width=30, height=20, bg='black', fg='red', font=("Courier", 12))  # Increase font size
for attack in attack_prevalence:
    listbox_attacks.insert(tk.END, attack)
listbox_attacks.grid(row=0, column=0, padx=5, pady=5, sticky=tk.N+tk.S)
scrollbar_attacks = tk.Scrollbar(frame_attacks, orient=tk.VERTICAL, command=listbox_attacks.yview)
scrollbar_attacks.grid(row=0, column=1, sticky=tk.N+tk.S)
listbox_attacks.config(yscrollcommand=scrollbar_attacks.set)

# Attack Description
frame_description = tk.LabelFrame(app, text="Attack Description", bg='black')
frame_description.grid(row=0, column=1, padx=10, pady=10, sticky=tk.N+tk.S)

text_description = scrolledtext.ScrolledText(frame_description, width=50, height=20, wrap=tk.WORD, bg='black', fg='skyblue', font=("Courier", 12))  # Increase font size
text_description.grid(row=0, column=0, padx=5, pady=5)

# Frame for Pie Chart
frame_chart = tk.LabelFrame(app, text="Pie Chart")
frame_chart.grid(row=0, column=2, padx=10, pady=10, sticky=tk.N+tk.S)

# Function to generate pie chart
def generate_pie_chart():
    fig, ax = plt.subplots(figsize=(8, 8))  # Adjust pie chart size here
    ax.pie(list(attack_prevalence.values()), labels=list(attack_prevalence.keys()), autopct='%1.1f%%', textprops={'fontsize': 10})  # Increase font size for pie chart labels
    ax.set_title("Prevalence of Cyber Attacks", fontsize=12)  # Increase font size for pie chart title
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    canvas = FigureCanvasTkAgg(fig, master=frame_chart)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

generate_pie_chart()

# Bind the listbox to the show_attack_details function
listbox_attacks.bind('<<ListboxSelect>>', show_attack_details)

# Button to show pie chart
button_show_pie_chart = tk.Button(app, text="Show Pie Chart", command=generate_pie_chart, font=("Courier", 12))  # Increase font size
button_show_pie_chart.grid(row=1, column=0, pady=10)

# Exit Button
exit_button = tk.Button(app, text="Exit", command=app.quit, bg="black", fg="red", font=("Courier", 12))  # Increase font size
exit_button.grid(row=1, column=2, pady=10)

# Function to open link in default web browser
def open_link():
    selected_attack = listbox_attacks.get(listbox_attacks.curselection())
    link = attack_descriptions[selected_attack]["Link"]
    import webbrowser
    webbrowser.open_new_tab(link)

# Button to open link for more information
button_more_info = tk.Button(app, text="More Info", command=open_link, font=("Courier", 12))  # Increase font size
button_more_info.grid(row=1, column=1, pady=10)

app.mainloop()
