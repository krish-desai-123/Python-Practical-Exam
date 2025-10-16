import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class FitnessTracker:

    def __init__(self, file_path):

        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])

    def log_activity(self, activity_type, duration, calories):

        new_entry = pd.DataFrame([{
            'Date': datetime.now(),
            'Activity Type': activity_type,
            'Duration (Minutes)': duration,
            'Calories Burned': calories
        }])
        self.df = pd.concat([self.df, new_entry], ignore_index=True)
        self.df.to_csv(self.file_path, index=False)
        print(f"\nActivity '{activity_type}' logged successfully.")

    def calculate_metrics(self):

        if self.df.empty:
            return None
        metrics = {
            "Total Calories": self.df['Calories Burned'].sum(),
            "Average Duration": np.mean(self.df['Duration (Minutes)']),
            "Activity Frequency": self.df['Activity Type'].value_counts()
        }
        return metrics

    def generate_report(self):

        metrics = self.calculate_metrics()
        if not metrics:
            print("\nNo data available to generate a report.")
            return

        print("\n--- Fitness Summary Report ---")
        print(f"Total Calories Burned: {metrics['Total Calories']:.2f} kcal")
        print(f"Average Activity Duration: {metrics['Average Duration']:.2f} minutes")
        print("\n--- Activity Frequency ---")
        print(metrics['Activity Frequency'].to_string())
        print("----------------------------\n")

    def filter_activities(self, condition, value):

        if self.df.empty:
            print("\nNo activities to filter.")
            return

        if condition == 'type':
            result_df = self.df[self.df['Activity Type'].str.lower() == value.lower()]
        elif condition == 'date':
            try:
                filter_date = pd.to_datetime(value).date()
                result_df = self.df[self.df['Date'].dt.date == filter_date]
            except ValueError:
                print("Invalid date format. Use YYYY-MM-DD.")
                return
        else:
            return

        if result_df.empty:
            print(f"\nNo activities found for '{value}'.")
        else:
            print(f"\n--- Filtered Results for '{value}' ---")
            print(result_df.to_string(index=False))

    def show_visualizations(self):

        if self.df.empty:
            print("\nNot enough data to create visualizations.")
            return

        print("\n--- Visualization Menu ---")
        print("1. Bar Chart (Time per Activity)")
        print("2. Line Graph (Calories Over Time)")
        print("3. Pie Chart (Activity Distribution)")
        print("4. Heatmap (Correlation)")
        choice = input("Choose a visualization (1-4): ")

        # --- Bar Chart ---
        if choice == '1':
            plt.figure(figsize=(10, 6))
            duration_by_activity = self.df.groupby('Activity Type')['Duration (Minutes)'].sum()
            sns.barplot(x=duration_by_activity.index, y=duration_by_activity.values)
            plt.title('Total Time Spent on Each Activity Type')
            plt.ylabel('Total Duration (Minutes)')
            plt.show()
        # --- Line Graph ---
        elif choice == '2':
            if self.df.shape[0] < 2:
                print("Need at least two entries for a line graph.")
                return
            calories_by_date = self.df.groupby(self.df['Date'].dt.date)['Calories Burned'].sum()
            plt.figure(figsize=(12, 6))
            calories_by_date.plot(kind='line', marker='o', grid=True)
            plt.title('Calories Burned Over Time')
            plt.ylabel('Calories Burned')
            plt.show()
        # --- Pie Chart ---
        elif choice == '3':
            activity_counts = self.df['Activity Type'].value_counts()
            plt.figure(figsize=(8, 8))
            plt.pie(activity_counts, labels=activity_counts.index, autopct='%1.1f%%', startangle=140)
            plt.title('Percentage Distribution of Activities')
            plt.axis('equal')
            plt.show()
        # --- Heatmap ---
        elif choice == '4':
            if self.df.shape[0] < 2:
                print("Need at least two entries for a heatmap.")
                return
            numeric_df = self.df[['Duration (Minutes)', 'Calories Burned']]
            correlation_matrix = numeric_df.corr()
            sns.heatmap(correlation_matrix, annot=True, cmap='viridis', fmt=".2f")
            plt.title('Correlation Between Duration and Calories Burned')
            plt.show()
        else:
            print("Invalid choice.")


def get_positive_float_input(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value > 0:
                return value
            else:
                print("Value must be a positive number.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def main():

    tracker = FitnessTracker('fitness_activities.csv')

    while True:
        print("\n===== Fitness Tracker Menu =====")
        print("1. Log Activity")
        print("2. Generate Report")
        print("3. Filter Activities")
        print("4. Show Visualizations")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            activity_type = input("Enter activity type: ")
            duration = get_positive_float_input("Enter duration in minutes: ")
            calories = get_positive_float_input("Enter calories burned: ")
            tracker.log_activity(activity_type, duration, calories)
        elif choice == '2':
            tracker.generate_report()
        elif choice == '3':
            filter_type = input("Filter by 'type' or 'date'?: ").lower()
            if filter_type in ['type', 'date']:
                value = input(f"Enter the {filter_type} to filter by: ")
                tracker.filter_activities(filter_type, value)
            else:
                print("Invalid filter option.")
        elif choice == '4':
            tracker.show_visualizations()
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please select an option from 1 to 5.")


if __name__ == "__main__":
    main()