import pandas as pd

# Load the symptom-to-category mapping CSV
mapping_df = pd.read_csv('sym_long.csv')
# Convert the DataFrame to a dictionary
symptom_to_categories = mapping_df.groupby('symptom')['category'].apply(list).to_dict()

def classify_terms(terms):
    category_mapping = {}
    
    for term in terms:
        # Check for the special case
        if term == "No symptom detected":
            category_mapping[term] = ["No category"]
        else:
            category_mapping[term] = symptom_to_categories.get(term, ["Unknown category"])
    
    return category_mapping

