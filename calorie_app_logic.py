import json
import os
from datetime import datetime

class CalorieAppLogic:
    def __init__(self):
        self.user_info_log = self.load_log("user_info_log.json", default_type="list")
        self.food_log = self.load_log("food_log.json", default_type="dict")
        self.workout_log = self.load_log("workout_log.json", default_type="dict")

    def load_log(self, filename, default_type="dict"):
        """Loads the JSON log, returns an empty list or dict based on default_type."""
        if os.path.exists(filename):
            with open(filename, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    # If error occurs, return default_type (empty dict/list)
                    return [] if default_type == "list" else {}
        return [] if default_type == "list" else {}

    def save_log(self, filename, data):
        """Saves the given data to the specified filename."""
        with open(filename, "w") as file:
            json.dump(data, file, indent=4)

    def save_personal_info(self, name, age, weight, gender, goal):
        """Saves new personal info to user_info_log."""
        try:
            new_user_info = {
                "name": name,
                "age": int(age),
                "weight": float(weight),
                "gender": gender,
                "goal": float(goal)
            }
            self.user_info_log.append(new_user_info)
            self.save_log("user_info_log.json", self.user_info_log)
        except ValueError as e:
            print(f"Error in saving personal info: {e}")
            return False
        return True

    def log_food(self, date, food_item, servings, calories):
        """Logs food entry for the given date."""
        try:
            servings = float(servings)
            calories = float(calories)
            total_calories = servings * calories

            self.food_log.setdefault(date, []).append({
                "food": food_item,
                "servings": servings,
                "calories": total_calories
            })

            self.save_log("food_log.json", self.food_log)
            return total_calories  # Return the calculated total calories
        except ValueError as e:
            print(f"Error in logging food: {e}")
            return None  # Return None if there was an error with the input

    def clear_food_log(self):
        """Clears the food log."""
        self.food_log = {}
        self.save_log("food_log.json", self.food_log)

    def log_workout(self, date, exercise, duration, calories_burned):
        """Logs workout data for the given date."""
        try:
            workout_entry = {
                "exercise": exercise,
                "duration": float(duration),
                "calories_burned": float(calories_burned)
            }
            self.workout_log.setdefault(date, []).append(workout_entry)
            self.save_log("workout_log.json", self.workout_log)
        except ValueError as e:
            print(f"Error in logging workout: {e}")
            return False
        return True

    def get_goal_for_date(self, date):
        """Retrieve the goal for a specific date from user info."""
        for user_info in self.user_info_log:
            # Assuming user goal is constant for all days (or can be modified by date)
            return user_info.get("goal", 0)
        return 0  # Default if no goal is set

    def update_calorie_summary(self):
        """Generates and returns a summary of calorie intake and burn for each day."""
        summary_lines = []
        all_dates = set(self.food_log.keys()) | set(self.workout_log.keys())

        for date in sorted(all_dates):
            # Get total food calories for the day (calories in)
            food_total = sum(entry["calories"] for entry in self.food_log.get(date, []))
            
            # Get total workout calories burned for the day (calories out)
            workout_total = sum(entry["calories_burned"] for entry in self.workout_log.get(date, []))
            
            # Get the net calories: food_total - workout_total
            net = food_total - workout_total
            
            # Get the goal for that date (user's input goal for the day)
            goal = self.get_goal_for_date(date)

            # Format the date as MM/DD/YYYY (the format you are using)
            try:
                formatted_date = datetime.strptime(date, "%m/%d/%Y").strftime("%m/%d/%Y")
            except ValueError:
                # If parsing fails, handle the error gracefully
                print(f"Error parsing date: {date}")
                formatted_date = date  # Keep original if date parsing fails

            # Create the summary line with goal, food calories, workout calories, net calories, and difference from goal
            summary_lines.append(
                f"{formatted_date}: Goal: {goal:.0f} kcal, "
                f"Food: {food_total:.0f} kcal in, "
                f"Workout: {workout_total:.0f} kcal out "
                f"(Net: {net:.0f} kcal, Diff: {net - goal:+})"
            )

        return "\n".join(summary_lines)

    def clear_calorie_summary(self):
        """Clears the food log, workout log, and resets calorie data."""
        self.food_log = {}  # Clear the food log
        self.workout_log = {}  # Clear the workout log
        self.save_log("food_log.json", self.food_log)  # Save the cleared food log
        self.save_log("workout_log.json", self.workout_log)  # Save the cleared workout log
