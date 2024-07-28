import customtkinter as ctk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import requests
from bs4 import BeautifulSoup

class DomainSearchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Domain Search & Web Browser")
        self.geometry("800x600")
        self.configure(bg="#1F1F1F")  # Dark background color

        # Load the domain data
        self.df = pd.read_csv('url set1.csv')

        # Initialize variables
        self.current_domain_info = None

        # Create frames for displaying results
        self.left_frame = ctk.CTkFrame(self, fg_color="#1F1F1F")
        self.left_frame.pack(side=ctk.LEFT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

        self.right_frame = ctk.CTkFrame(self, fg_color="#1F1F1F")
        self.right_frame.pack(side=ctk.RIGHT, padx=10, pady=10, expand=True, fill=ctk.BOTH)

        # Left Frame Widgets
        self.label = ctk.CTkLabel(self.left_frame, text="Enter Domain:", text_color="skyblue")
        self.label.pack()

        self.entry = ctk.CTkEntry(self.left_frame, fg_color="#2F2F2F", text_color="white", width=500)  # Increased width
        self.entry.pack(pady=10)  # Added padding for better spacing

        self.search_button = ctk.CTkButton(self.left_frame, text="Search", command=self.search_domain, fg_color="black", text_color="skyblue")
        self.search_button.pack()

        self.listbox = ctk.CTkTextbox(self.left_frame, width=40, height=10, fg_color="#2F2F2F", text_color="white")
        self.listbox.pack(side=ctk.TOP, padx=10, pady=10, expand=True, fill=ctk.BOTH)

        # Right Frame Widgets
        self.result_text = ctk.CTkTextbox(self.right_frame, wrap=ctk.WORD, fg_color="#2F2F2F", text_color="skyblue")
        self.result_text.pack(fill=ctk.BOTH, expand=True)

        self.analyze_button = ctk.CTkButton(self.right_frame, text="Analyze URL", command=self.analyze_url, fg_color="black", text_color="skyblue")
        self.analyze_button.pack(side=ctk.TOP, padx=10, pady=10)

        self.exit_button = ctk.CTkButton(self.right_frame, text="Exit", command=self.quit, fg_color="black", text_color="skyblue")
        self.exit_button.pack(side=ctk.BOTTOM, padx=10, pady=10)

    def search_domain(self):
        url = self.entry.get().lower()  # Convert input to lowercase for case-insensitive matching
        domain_info = self.df[self.df['url'].str.lower().str.contains(url, regex=False)]

        if not domain_info.empty:
            # Display non-malicious pie chart
            self.display_pie_chart([0, 100])
            self.current_domain_info = domain_info
        else:
            # Attempt to fetch the webpage
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    # Display non-malicious pie chart
                    self.display_pie_chart([0, 100])
                else:
                    # Display malicious pie chart
                    self.display_pie_chart([100, 0])
            except Exception as e:
                # Display malicious pie chart
                self.display_pie_chart([100, 0])
                print(f"Error fetching URL: {e}")

        self.listbox.delete(1.0, ctk.END)
        self.current_domain_info = None

    def display_pie_chart(self, sizes):
        labels = ['Malicious', 'Non-Malicious']

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=['red', 'green'])
        ax.set_title('Malicious vs Non-Malicious', color='skyblue')
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(fig, master=self.left_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def analyze_url(self):
        url = self.entry.get()
        analyze_info = self.get_url_analyze_info(url)
        self.display_url_analyze_info(analyze_info)

    def get_url_analyze_info(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('title').get_text() if soup.find('title') else 'N/A'
            return f"Title: {title}\nURL: {url}\n" \
                   f"\nInput analyze info: This is your analyze info for {url}."
        except Exception as e:
            return f"Error analyzing URL: {url}\n{e}"

    def display_url_analyze_info(self, analyze_info):
        self.result_text.delete(1.0, ctk.END)
        self.result_text.insert(ctk.END, analyze_info)

if __name__ == "__main__":
    app = DomainSearchApp()
    app.mainloop()
