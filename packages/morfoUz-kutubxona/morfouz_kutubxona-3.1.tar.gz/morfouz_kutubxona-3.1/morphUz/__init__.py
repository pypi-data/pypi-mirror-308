import pandas as pd
import re

# Attempt to read the CSV file with an alternative encoding
try:
    root_words_df = pd.read_csv('root.csv', encoding='utf-8')  # First, try utf-8
except UnicodeDecodeError:
    try:
        root_words_df = pd.read_csv('root.csv', encoding='ISO-8859-1')  # Try ISO-8859-1
    except UnicodeDecodeError:
        root_words_df = pd.read_csv('root.csv', encoding='cp1252')  # Try cp1252

# The rest of your code remains the same...

# Define suffixes and categories (update these based on language needs)
suffixes = {
    'verb': ['yap', 'yab', 'moqda', 'yotir', 'di', 'gan', 'kan', 'ib', 'bdi',
'moqchi', 'ajak', 'uraman', 'ing', 'i', 'gil', 'sin', 'il', 'in', 'l', 'dir',
'sa', 'sin', 'sam', 'sin', 'sak', 'sa', 'edi', 'moq', 'mog`i', 'kerak', 'sin',
'man', 'san', 'di', 'miz', 'ingiz', 'lar', 'moqqa', 'gani', 'lab', 'liq', 'lash',
'ibdi', 'holda', 'ar', 'turmoq', 'tar', 'gim',  'keldi', 'ng', 'yapman'],
    
    'noun': ['larni', 'lar', 'im', 'ing', 'i', 'miz', 'ingiz', 'lari', 'cha', 'gina', 'qay', 
    'jig`', 'chak', 'chi', 'lik', 'chilik', 'joy', 'goh', 'xona', 'li', 'lamoq', 
    'qo`q', 'ist', 'gar', 'zor', 'simon', 'moq', 'garlik', 'on', 'kon', 'lash', 
    'nchi', 'dan', 'siz'],
    
    'adj': ['li', 'siz', 'dor', 'viy', 'gina', 'qina', 'roq', 'tar', 'simon', 'day',
            'cha', 'qay', 'chi', 'shunos', 'goh', 'zor'],

    'pronoun': ['im', 'ing', 'i', 'imiz', 'ingiz', 'lari', 'niki', 'imniki', 
'o`zi', 'o`zing', 'o`zim', 'larim', 'laringiz', 'miz', 'mizni', 'imizning'],

    'number': ['inchi', 'nchi', 'marta', 'talik', 'lik', 'inchi', 'ta', 'talik', 'lab'],
    
    'adverb': ['cha', 'lab', 'layin', 'g`oncha', 'lashincha', 'roq']

}

def load_roots():
    """Load root words from root.csv into a dictionary for faster lookup."""
    root_dict = {row['lotin']: row['turkum'] for _, row in root_words_df.iterrows()}
    return root_dict

def find_root_and_suffix(word, root_dict):
    """
    Split a word into root and suffixes if possible.
    Returns root, suffix, and category.
    """
    for suffix_type, suffix_list in suffixes.items():
        for suffix in suffix_list:
            if word.endswith(suffix):
                possible_root = word[:-len(suffix)]
                if possible_root in root_dict:
                    return possible_root, suffix, root_dict[possible_root]
    # If no suffix found, treat entire word as root
    return word, None, root_dict.get(word, 'unknown')

def morphological_analysis(sentence, root_dict):
    """
    Analyzes each word in a sentence, identifying roots and suffixes.
    """
    results = []
    words = [re.sub(r'[^\w\s`]', '', word.replace('’', '`')) for word in sentence.split()]
    for word in words:
        root, suffix, category = find_root_and_suffix(word, root_dict)
        results.append({
            'word': word,
            'root': root,
            'suffix': suffix,
            'category': category
        })
    return results

# Load roots into a dictionary for quick access
root_dict = load_roots()

# Example usage
sentence = input("O`zbek tilidagi matn kiriting: ")
analysis_results = morphological_analysis(sentence, root_dict)

# Display results
for result in analysis_results:
    print(f"Word: {result['word']}, Root: {result['root']}, Suffix: {result['suffix']}, Category: {result['category']}")
