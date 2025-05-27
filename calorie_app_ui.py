import tkinter as tk
from tkinter import messagebox, ttk
from calorie_app_logic import CalorieAppLogic


class CalorieAppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")
        self.root.geometry("600x500")

        self.logic = CalorieAppLogic()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.build_ui()

    def create_tab(self, title, frame):
        self.notebook.add(frame, text=title)

    def build_ui(self):
        self.create_personal_info_tab()
        self.create_log_food_tab()
        self.create_log_workout_tab()

    def create_personal_info_tab(self):
        tab = ttk.Frame(self.notebook)

        self.name_label = ttk.Label(tab, text="Name:")
        self.name_label.pack(padx=10, pady=5)
        self.name_entry = ttk.Entry(tab)
        self.name_entry.pack(padx=10, pady=5)

        self.age_label = ttk.Label(tab, text="Age:")
        self.age_label.pack(padx=10, pady=5)
        self.age_entry = ttk.Entry(tab)
        self.age_entry.pack(padx=10, pady=5)

        self.weight_label = ttk.Label(tab, text="Weight (lbs):")
        self.weight_label.pack(padx=10, pady=5)
        self.weight_entry = ttk.Entry(tab)
        self.weight_entry.pack(padx=10, pady=5)

        self.gender_label = ttk.Label(tab, text="Gender:")
        self.gender_label.pack(padx=10, pady=5)
        self.gender_entry = ttk.Entry(tab)
        self.gender_entry.pack(padx=10, pady=5)

        self.goal_label = ttk.Label(tab, text="Daily Calorie Goal:")
        self.goal_label.pack(padx=10, pady=5)
        self.goal_entry = ttk.Entry(tab)
        self.goal_entry.pack(padx=10, pady=5)

        submit_button = ttk.Button(tab, text="Save Info", command=self.save_personal_info)
        submit_button.pack(padx=20, pady=10)

        clear_button = ttk.Button(tab, text="Clear Entries", command=self.clear_personal_info_log)
        clear_button.pack(padx=20, pady=5)

        self.personal_info_log = tk.Text(tab, wrap="word", width=50, height=10)
        self.personal_info_log.pack(padx=10, pady=10)

        self.update_personal_info_log()
        self.create_tab("Personal Info", tab)

    def save_personal_info(self):
        name = self.name_entry.get()
        age = self.age_entry.get()
        weight = self.weight_entry.get()
        gender = self.gender_entry.get()
        goal = self.goal_entry.get()

        if not name or not age.isdigit() or not weight.replace('.', '', 1).isdigit() \
           or not gender or not goal.replace('.', '', 1).isdigit():
            messagebox.showerror("Input Error", "Please provide valid inputs for all fields.")
            return

        self.logic.save_personal_info(name, age, weight, gender, goal)
        self.update_personal_info_log()
        self.clear_personal_info_entries()

        messagebox.showinfo("Info Saved", "Personal information saved successfully.")

    def update_personal_info_log(self):
        self.personal_info_log.delete(1.0, tk.END)
        for user_info in self.logic.user_info_log:
            info_str = f"Name: {user_info['name']}\nAge: {user_info['age']}\n" \
                       f"Weight: {user_info['weight']} lbs\nGender: {user_info['gender']}\n" \
                       f"Goal: {user_info['goal']}\n\n"
            self.personal_info_log.insert(tk.END, info_str)

    def clear_personal_info_entries(self):
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)
        self.gender_entry.delete(0, tk.END)
        self.goal_entry.delete(0, tk.END)

    def clear_personal_info_log(self):
        self.logic.user_info_log.clear()
        self.logic.save_log("user_info_log.json", self.logic.user_info_log)
        self.personal_info_log.delete(1.0, tk.END)
        messagebox.showinfo("Info Cleared", "All personal info entries have been cleared.")

    def create_log_food_tab(self):
        tab = ttk.Frame(self.notebook)

        ttk.Label(tab, text="Date (MM/DD/YYYY):").pack(pady=5)
        self.food_date_entry = ttk.Entry(tab)
        self.food_date_entry.pack(pady=5)

        ttk.Label(tab, text="Food:").pack(pady=5)
        self.food_item_entry = ttk.Entry(tab)
        self.food_item_entry.pack(pady=5)

        ttk.Label(tab, text="Servings:").pack(pady=5)
        self.servings_entry = ttk.Entry(tab)
        self.servings_entry.pack(pady=5)

        ttk.Label(tab, text="Calories per Serving:").pack(pady=5)
        self.calories_entry = ttk.Entry(tab)
        self.calories_entry.pack(pady=5)

        log_button = ttk.Button(tab, text="Log Food", command=self.log_food)
        log_button.pack(pady=10)

        clear_button = ttk.Button(tab, text="Clear Entries", command=self.clear_food_entries)
        clear_button.pack(pady=5)

        self.food_log_text = tk.Text(tab, wrap="word", width=60, height=10)
        self.food_log_text.pack(padx=10, pady=10)
        self.food_log_text.insert(tk.END, "Food Log\n")

        self.calorie_summary_label = ttk.Label(tab, text="", font=("Arial", 12, "bold"))
        self.calorie_summary_label.pack(pady=10)

        clear_summary_button = ttk.Button(tab, text="Clear Summary", command=self.clear_calorie_summary)
        clear_summary_button.pack(pady=5)

        self.create_tab("Log Food", tab)
        self.update_calorie_summary()
        self.populate_food_log_text()

    def log_food(self):
        date = self.food_date_entry.get()
        food_item = self.food_item_entry.get()
        servings = self.servings_entry.get()
        calories = self.calories_entry.get()

        if not date or not food_item or not servings or not calories:
            messagebox.showerror("Input Error", "Please fill out all fields.")
            return

        try:
            servings = float(servings)
            calories = float(calories)

            total_calories = self.logic.log_food(date, food_item, servings, calories)

            if total_calories is not None:
                self.food_log_text.insert(tk.END, f"{date}: {food_item} x {servings} = {total_calories} cal\n")
                self.update_calorie_summary()
            else:
                messagebox.showerror("Error", "Failed to log food.")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for servings and calories.")

    def clear_food_entries(self):
        self.food_log_text.delete(1.0, tk.END)
        self.food_log_text.insert(tk.END, "Food Log\n")
        self.logic.clear_food_log()

    def populate_food_log_text(self):
        self.food_log_text.delete(1.0, tk.END)
        self.food_log_text.insert(tk.END, "Food Log\n")
        for date, entries in self.logic.food_log.items():
            for entry in entries:
                self.food_log_text.insert(
                    tk.END,
                    f"{date}: {entry['food']} x {entry['servings']} = {entry['calories']} cal\n"
                )

    def create_log_workout_tab(self):
        tab = ttk.Frame(self.notebook)

        ttk.Label(tab, text="Date (MM/DD/YYYY):").pack(pady=5)
        self.workout_date_entry = ttk.Entry(tab)
        self.workout_date_entry.pack(pady=5)

        ttk.Label(tab, text="Exercise:").pack(pady=5)
        self.exercise_entry = ttk.Entry(tab)
        self.exercise_entry.pack(pady=5)

        ttk.Label(tab, text="Duration (minutes):").pack(pady=5)
        self.duration_entry = ttk.Entry(tab)
        self.duration_entry.pack(pady=5)

        ttk.Label(tab, text="Calories Burned:").pack(pady=5)
        self.calories_burned_entry = ttk.Entry(tab)
        self.calories_burned_entry.pack(pady=5)

        submit_button = ttk.Button(tab, text="Log Workout", command=self.log_workout)
        submit_button.pack(pady=10)

        clear_button = ttk.Button(tab, text="Clear Entries", command=self.clear_workout_entries)
        clear_button.pack(pady=5)

        self.recent_workout_log_text = tk.Text(tab, wrap="word", width=60, height=10)
        self.recent_workout_log_text.pack(padx=10, pady=10)
        self.recent_workout_log_text.insert(tk.END, "Workout Log\n")

        self.create_tab("Log Workout", tab)

    def log_workout(self):
        date = self.workout_date_entry.get().strip()
        exercise = self.exercise_entry.get().strip()
        duration = self.duration_entry.get().strip()
        calories_burned = self.calories_burned_entry.get().strip()

        if not date or not exercise or not duration or not calories_burned:
            messagebox.showerror("Input Error", "Please fill out all fields.")
            return

        try:
            duration = float(duration)
            calories_burned = float(calories_burned)

            self.logic.log_workout(date, exercise, duration, calories_burned)

            self.recent_workout_log_text.insert(
                tk.END,
                f"{date}: {exercise} - {calories_burned} cal burned in {duration} min\n"
            )
            self.update_calorie_summary()
            self.clear_workout_entries()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for duration and calories.")

    def clear_workout_entries(self):
        self.workout_date_entry.delete(0, tk.END)
        self.exercise_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.calories_burned_entry.delete(0, tk.END)

    def update_calorie_summary(self):
        summary = self.logic.update_calorie_summary()
        self.calorie_summary_label.config(text=summary)

    def clear_calorie_summary(self):
        self.logic.clear_calorie_summary()  # Make sure you have a method in the logic to clear summary data
        self.calorie_summary_label.config(text="")
        messagebox.showinfo("Summary Cleared", "Calorie summary has been cleared.")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieAppUI(root)
    root.mainloop()

