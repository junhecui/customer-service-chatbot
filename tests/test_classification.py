import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from classification import classify_inquiry

# Testing dataset for classifying queries
test_data = [
    {"query": "Can you remind me to study for my test tomorrow?", "ground_truth_category": "Reminders"},
    {"query": "Book a meeting with James at 4PM on Tuesday", "ground_truth_category": "Scheduling"},
    {"query": "Organize my to-do list from least to most urgent", "ground_truth_category": "Task Management"},
    {"query": "Send an email to Jordan Thompson asking for an update on the project", "ground_truth_category": "Communication"},
    {"query": "Find me a cheap fast food restaurant to order from", "ground_truth_category": "Recommendations"},
    {"query": "What's the weather like today?", "ground_truth_category": "Information Retrieval"},
    {"query": "I need help with something else", "ground_truth_category": "General Assistance"}
]

# Calculate classification accuracy
correct_classifications = 0
for item in test_data:
    predicted_category = classify_inquiry(item["query"])
    if predicted_category == item["ground_truth_category"]:
        correct_classifications += 1
    else:
        print(item["ground_truth_category"], predicted_category)
accuracy = (correct_classifications / len(test_data)) * 100
print(f"Classification Accuracy: {accuracy:.2f}%")