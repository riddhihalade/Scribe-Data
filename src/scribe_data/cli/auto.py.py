import argparse
import sys
from scribe_data.process_wiki import gen_autosuggestions  
from SPARQLWrapper import SPARQLWrapper, JSON

# Define the SPARQL endpoint
SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"

def fetch_language_data(language, data_type):
    """
    Fetch language data from Wikidata using SPARQL.
    """
    sparql = SPARQLWrapper(SPARQL_ENDPOINT)
    query = f"""
        SELECT ?item ?itemLabel
        WHERE {{
            ?item wdt:P31 wd:{data_type}.
            ?item wdt:P407 wd:{language}.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    return results["results"]["bindings"]

def handle_autosuggestions(language):
    """
    Generate autosuggestions using Wikipedia data.
    """
    suggestions = gen_autosuggestions(language)  # Call the autosuggestions generator
    return suggestions

def main():
    parser = argparse.ArgumentParser(description="Get language data from Wikidata.")
    
    # Define the arguments
    parser.add_argument("-lang", required=True, help="Language code (e.g., en for English).")
    parser.add_argument("-dt", required=True, help="Data type (e.g., Q5 for human).")
    parser.add_argument("--autosuggest", action="store_true", help="Enable autosuggestions.")
    
    args = parser.parse_args()
    
    language = args.lang
    data_type = args.dt

    # Fetch language data from Wikidata
    print(f"Fetching data for language: {language}, data type: {data_type}...")
    data = fetch_language_data(language, data_type)
    
    # Display fetched data
    if data:
        print(f"Data fetched for language {language} and type {data_type}:")
        for item in data:
            print(f" - {item['itemLabel']['value']} ({item['item']['value']})")
    else:
        print(f"No data found for language {language} and type {data_type}.")
    
    # Handle autosuggestions if enabled
    if args.autosuggest:
        print(f"Generating autosuggestions for {language}...")
        suggestions = handle_autosuggestions(language)
        if suggestions:
            print("Autosuggestions:")
            for suggestion in suggestions:
                print(f" - {suggestion}")
        else:
            print("No autosuggestions generated.")
    
if __name__ == "__main__":
    main()
