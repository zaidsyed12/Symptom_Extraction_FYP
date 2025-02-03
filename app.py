from model import apply
from postprocessing import classify_terms

def main():
    print("Symptom Detection and Categorization")
    print("------------------------------------")
    while True:
        input_text = input("\nEnter medical text (or type 'exit' to quit): ").strip()
        
        if input_text.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break
        
        # Apply symptom detection
        entities = apply(input_text)
        
        # Categorize the detected symptoms
        entity_categories = classify_terms(entities)
        
        # Display the results

#        print("\nExtracted Symptoms:")
#        for entity, categories in entity_categories.items():
#            print(f"- {entity}: {', '.join(categories)}")

        print("\nExtracted Symptoms:")
        for entity, categories in entity_categories.items():
            print(f"- {entity}")


if __name__ == "__main__":
    main()
