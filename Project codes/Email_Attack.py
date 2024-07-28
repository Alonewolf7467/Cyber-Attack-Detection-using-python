import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import re

# Spam type dictionary
spam_types = {
    "phishing": {
        "spam_description": "Emails disguised as real companies to steal personal information. (e.g., fake bank emails)",
        "process": "Spoofed sender address to appear legitimate (e.g., bank, social media platform).\nUrgent message urging action (e.g., verify account, update information).\nLink to a fake website mimicking the real one.\nSteals personal information (passwords, credit cards) entered on the fake site.",
        "disadvantages": "Identity theft, financial loss, malware infection.",
        "previous_attacks_count": "Millions per year",
        "preventions": "Don't click links or attachments in suspicious emails.\nVerify sender legitimacy before responding.\nUse strong passwords and enable two-factor authentication.",
        "reference_links": "https://www.ftc.gov/phishing-0"
    },
    "scareware": {
        "spam_description": "Emails warn of fake threats to pressure useless software download.",
        "process": "Warns of critical security issues or non-existent viruses.\nPressures download of fake security software (often malware).\nSteals data or charges for useless software.",
        "disadvantages": "Malware infection, data theft, financial loss.",
        "previous_attacks_count": "Hundreds of millions per year",
        "preventions": "Be cautious of unsolicited security warnings.\nUpdate your antivirus software regularly.\nDon't download software from suspicious emails.",
        "reference_links": "https://en.wikipedia.org/wiki/Scareware"
    },
    "lottery": {
        "spam_description": "Emails announce fake prizes to steal money or information.",
        "process": "Announces a large prize you never entered.\nCreates urgency to claim the prize with a response.\nRequests upfront fees or personal information to 'process' the claim.\nSteals money or personal information.",
        "disadvantages": "Financial loss, identity theft.",
        "previous_attacks_count": "Millions per year",
        "preventions": "Don't respond to emails about unsolicited prizes.\nLegitimate lotteries won't ask for upfront fees.\nBe wary of emails with grammatical errors or urgency.",
        "reference_links": "https://en.wikipedia.org/wiki/Lottery_fraud"
    },
    "work from home": {
        "spam_description": "Emails promise easy jobs but steal money or information.",
        "process": "Promises high income for minimal work.\nOften involves upfront fees for 'training materials' or 'processing'.\nMay involve pyramid schemes or data collection.\nSteals money or personal information.",
        "disadvantages": "Financial loss, wasted time.",
        "previous_attacks_count": "Millions per year",
        "preventions": "Research job opportunities thoroughly.\nBeware of offers that seem too good to be true.\nLegitimate jobs won't ask for upfront fees.",
        "reference_links": "https://www.indeed.com/career-advice/finding-a-job/work-from-home-scams"
    },
    "blackmail": {
        "spam_description": "Emails threaten to expose embarrassing information about the recipient unless they pay a ransom or perform a specific action.",
        "process": "Threatens to reveal compromising information (often fabricated).\nDemands money or action to prevent the information from being exposed.\nMay contain a fake timer to increase urgency.",
        "disadvantages": "Emotional distress, financial loss, reputational damage.",
        "previous_attacks_count": "Difficult to quantify due to under-reporting.",
        "preventions": "Don't engage with the sender.\nReport the email to your email provider and law enforcement (if applicable).\nChange passwords for any accounts potentially compromised.",
        "reference_links": "https://reportfraud.ftc.gov/"
    },
    "malware": {
        "spam_description": "Disguised emails with attachments or links that, when clicked, download malware onto the recipient's device.",
        "process": "Appears legitimate with enticing content or subject lines.\nContains malicious attachments or links.\nDownloads malware upon clicking (e.g., viruses, ransomware).",
        "disadvantages": "Malware infection, data theft, identity theft, device damage.",
        "previous_attacks_count": "Hundreds of millions per year.",
        "preventions": "Be cautious of unsolicited attachments or links, even from seemingly familiar senders.\nUse strong spam filters and keep antivirus software updated.\nDon't enable macros in unsolicited documents.",
        "reference_links": "https://en.wikipedia.org/wiki/Malware"
    },
    "fake invoice": {
        "spam_description": "Emails mimic invoices from fake companies to steal money.",
        "process": "Spoofed Sender: The email appears to be from a legitimate company you may do business with, but the sender's address is actually fake.\nFake Invoice: The email includes an attachment or link that looks like a real invoice requesting payment for fake services or products.\nUrgency Tactic: The email creates a sense of urgency by demanding immediate payment to avoid penalties or service disruptions.\nPayment Trap: Clicking a link in the email or providing payment information can lead to fraudulent transactions, stealing your money.",
        "disadvantages": "Financial Loss: You could lose the money you send based on the fake invoice.\nData Breach: Clicking malicious links might expose your personal or financial information.",
        "previous_attacks_count": "Millions per year",
        "preventions": "Verify Sender Legitimacy: Don't trust the sender's name displayed in the email. Check the actual email address for inconsistencies or misspellings.\nContact Directly: If you have an account with the company mentioned in the invoice, contact them directly through their official channels (phone number or website) to verify its authenticity.\nInvoice Details Scrutiny: Carefully examine the invoice for errors, inconsistencies, or unfamiliar services.\nDon't Click Links: Avoid clicking on any links or opening attachments within the suspicious email.",
        "reference_links": ""
    }
}

# Keywords for spam detection
spam_keywords = {
    "phishing": [r"urgent", r"verify account", r"update information", r"bank", r"social media"],
    "scareware": [r"critical security", r"virus threat", r"attachment", r"download software"],
    "lottery": [r"lottery", r"winning notification", r"claim prize", r"lotto"],
    "work from home": [r"work from home", r"earn money online", r"easy job opportunity", r"part-time job"],
    "blackmail": [r"blackmail", r"reveal your secret", r"pay me or else", r"embarrassing video"],
    "malware": [r"download this file", r"click here for free", r"install now", r"your device is infected"],
    "fake invoice": [r"invoice", r"payment reminder", r"unpaid bill", r"pay now"],
}

# Load the model
def load_model():
    return None  # No need for ML model, using keyword-based detection

# Function to predict email category based on keywords
def predict_category(email_message):
    if email_message:
        matched_spam_types = []
        for spam_type, keywords in spam_keywords.items():
            for keyword in keywords:
                if re.search(keyword, email_message, re.IGNORECASE):
                    matched_spam_types.append(spam_type)
                    break
        if matched_spam_types:
            result_text = f"Detected Spam Types: {', '.join(matched_spam_types)}\n\n"
            for spam_type in matched_spam_types:
                result_text += f"Type of Spam: {spam_type}\n"
                for key, value in spam_types[spam_type].items():
                    if key != "reference_links":
                        result_text += f"{key.replace('_', ' ').title()}: {value}\n"
                result_text += "\n"
            return result_text
        else:
            return "No spam detected. This email appears to be Ham."
    else:
        return "Please enter an email message."

# App Class
class EmailSpamDetectorApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Email Spam Detector")
        self.geometry("950x600")

        # Create and pack widgets
        frame = ctk.CTkFrame(self)
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        email_label = ctk.CTkLabel(frame, text="Enter Email Message:")
        email_label.grid(row=0, column=1, sticky=tk.E)

        self.email_entry = ctk.CTkEntry(frame, width=300, height=50)
        self.email_entry.grid(row=0, column=2, sticky=tk.W, padx=10)

        predict_button = ctk.CTkButton(frame, text="Predict", command=self.predict_category)
        predict_button.grid(row=1, column=1, pady=(20, 0), padx=10)

        reset_button = ctk.CTkButton(frame, text="Check Another Email", command=self.reset_app)
        reset_button.grid(row=1, column=2, pady=(20, 0), padx=10)

        # Create exit button
        exit_button = ctk.CTkButton(self, text="Exit", command=self.destroy)
        exit_button.place(relx=1.0, rely=0.0, anchor=tk.NE)  # Place at top-right

        # Create result box
        self.result_frame = ctk.CTkFrame(self)
        self.result_frame.grid(row=1, column=0, columnspan=3, pady=(20, 0), padx=(20, 0), sticky=(tk.N, tk.E))

        self.result_label = ctk.CTkLabel(self.result_frame, text="Result: ", font=("Helvetica", 12))
        self.result_label.pack(anchor=tk.NW)

        # Create bar chart frame
        self.bar_chart_frame = ctk.CTkFrame(self)
        self.bar_chart_frame.grid(row=0, column=2, pady=(20, 0), padx=(20, 0), sticky=(tk.N, tk.W))
        self.bar_chart_label = ctk.CTkLabel(self.bar_chart_frame, text="Bar Chart", font=("Helvetica", 16))
        self.bar_chart_label.pack()
        self.bar_chart_canvas = ctk.CTkCanvas(self.bar_chart_frame, width=300, height=300)
        self.bar_chart_canvas.pack()

    # Function to predict category and update result label
    def predict_category(self):
        email_message = self.email_entry.get()
        prediction_result = predict_category(email_message)
        messagebox.showinfo("Prediction", prediction_result)
        self.update_result_label(prediction_result)
        self.update_bar_chart("spam" in prediction_result.lower())

    # Function to update result label
    def update_result_label(self, prediction):
        self.result_label.configure(text=prediction)

    # Function to update bar chart
    def update_bar_chart(self, is_spam):
        self.bar_chart_canvas.delete("all")
        if is_spam:
            self.bar_chart_canvas.create_rectangle(50, 50, 250, 250, fill="lightcoral")
            self.bar_chart_canvas.create_text(150, 20, text="Spam", font=("Helvetica", 12), anchor=tk.N)
            self.bar_chart_canvas.create_text(150, 280, text="100%", font=("Helvetica", 12), anchor=tk.N)
        else:
            self.bar_chart_canvas.create_rectangle(50, 50, 250, 250, fill="lightblue")
            self.bar_chart_canvas.create_text(150, 20, text="Ham", font=("Helvetica", 12), anchor=tk.N)
            self.bar_chart_canvas.create_text(150, 280, text="100%", font=("Helvetica", 12), anchor=tk.N)

    # Function to reset the app
    def reset_app(self):
        self.email_entry.delete(0, 'end')
        self.result_label.configure(text="Result: ")

if __name__ == "__main__":
    app = EmailSpamDetectorApp()
    app.mainloop()
