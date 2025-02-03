from tkinter import *
from tkinter import messagebox as tmsg
import customtkinter # type: ignore
from PIL import Image, ImageTk # type: ignore
import numpy as np # type: ignore
import joblib # type: ignore
from tkinter import ttk

class AQI_Predictor:
    def __init__(self):
        self.model_path = "./rf_model"
        self.icon_path = "./aqi_icon.ico"
        self.pattern_path = "./pattern.jpg"

        self.rf_model = joblib.load(self.model_path)

        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("green")

        self.main_window = customtkinter.CTk()
        self.main_window.geometry("1200x750")
        self.main_window.wm_iconbitmap(self.icon_path)
        self.main_window.title("AQI Predictor")

        bg_image = customtkinter.CTkImage(light_image=Image.open(self.pattern_path), dark_image=Image.open(self.pattern_path), size=(1200, 750))
        self.bg_label = customtkinter.CTkLabel(self.main_window, image=bg_image, text="")
        self.bg_label.pack()

        self.main_frame = customtkinter.CTkFrame(master=self.bg_label, width=900, height=600, corner_radius=20)
        self.main_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.pollutant_vars = {}
        pollutants = ["PM 2_5", "PM10", "NO", "NO2", "NOx", "NH3", "CO", "SO2", "O3", "Benzene", "Toluene", "Xylene"]
        
        title = customtkinter.CTkLabel(self.main_frame, text="Enter Pollutant Levels", font=("Montserrat", 25, "bold"))
        title.place(x=300, y=20)

        for i, pollutant in enumerate(pollutants):
            row, col = divmod(i, 2)
            self.pollutant_vars[pollutant] = StringVar()
            
            label = customtkinter.CTkLabel(self.main_frame, text=pollutant, font=("Montserrat", 15))
            label.place(x=50 + col * 400, y=80 + row * 50)
            entry = customtkinter.CTkEntry(self.main_frame, width=180, textvariable=self.pollutant_vars[pollutant])
            entry.place(x=180 + col * 400, y=80 + row * 50)

        self.result_label = customtkinter.CTkLabel(self.main_frame, text="", font=("Montserrat", 20, "bold"), text_color="white")
        self.result_label.place(x=350, y=450)
        
        self.aqi_gauge = customtkinter.CTkProgressBar(self.main_frame, width=500, height=20)
        self.aqi_gauge.place(x=200, y=500)
        self.aqi_gauge.set(0)

        predict_btn = customtkinter.CTkButton(self.main_frame, text="Predict AQI", command=self.get_aqi, width=200, height=50)
        predict_btn.place(x=250, y=550)
        
        quit_btn = customtkinter.CTkButton(self.main_frame, text="Quit", command=self.main_window.quit, width=200, height=50, fg_color="red")
        quit_btn.place(x=480, y=550)
        
        self.main_window.mainloop()

    def get_aqi(self):
        try:
            input_values = [float(self.pollutant_vars[pollutant].get()) for pollutant in self.pollutant_vars]
            input_array = np.array([input_values])
            prediction = self.rf_model.predict(input_array)[0]
            
            aqi_status = self.get_aqi_status(prediction)
            
            self.result_label.configure(text=f"AQI: {int(prediction)} | Status: {aqi_status}")
            self.aqi_gauge.set(min(prediction / 500, 1))
        
        except ValueError:
            tmsg.showerror("Error", "Please enter valid numeric values for all fields!")
    
    def get_aqi_status(self, aqi):
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Satisfactory"
        elif aqi <= 200:
            return "Moderately Polluted"
        elif aqi <= 300:
            return "Poor"
        elif aqi <= 400:
            return "Very Poor"
        elif aqi <= 500:
            return "Severe"
        else:
            return "Hazardous"

start = AQI_Predictor()
