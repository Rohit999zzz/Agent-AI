"""
Example usage scenarios for the AI Assistant
"""

examples = [
    {
        "query": "Search for the latest news about AI and then calculate the percentage increase if AI adoption went from 30% to 85%",
        "expected_flow": "WebSearch → Calculator"
    },
    {
        "query": "Read the sales_data.csv file and calculate the total revenue",
        "expected_flow": "FileReader → CSVAnalyzer"
    },
    {
        "query": "Find information about Python programming best practices and summarize the key points",
        "expected_flow": "WebSearch → Summary"
    },
    {
        "query": "Read this PDF report and calculate the average of the numbers mentioned in it",
        "expected_flow": "FileReader → Calculator"
    },
    {
        "query": "Calculate the compound interest for $1000 at 5% for 10 years using the formula A = P(1+r)^t",
        "expected_flow": "Calculator"
    },
    {
        "query": "Search for current Python trends and calculate what 25% of developers would be if there are 10 million developers worldwide",
        "expected_flow": "WebSearch → Calculator"
    }
]

def run_examples(assistant):
    """Run example queries to test the assistant"""
    print("🧪 Running Example Queries...\n")
    
    for i, example in enumerate(examples, 1):
        print(f"Example {i}: {example['query']}")
        print(f"Expected Flow: {example['expected_flow']}")
        print("-" * 50)
        
        try:
            response = assistant.chat(example['query'])
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    from enhanced_main import EnhancedPersonalAIAssistant
    assistant = EnhancedPersonalAIAssistant()
    run_examples(assistant) 