import pandas as pd

df = pd.read_csv('sparks_agi_leetcode_problems.csv')

task_ids = df["Task_ID"].tolist()
question_content = df["Question_Content"].tolist()
difficulty = df["Difficulty"].tolist()

print(task_ids)
print(question_content)
print(difficulty)