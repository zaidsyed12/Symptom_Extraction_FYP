import spacy
import re
import spacy_stanza
from negspacy.termsets import termset
from negspacy.negation import Negex


nlp = spacy.load("en_biobert_ner_symptom")

nlp_sz = spacy_stanza.load_pipeline("en", package="mimic", processors={"ner": "i2b2"})
ts = termset("en_clinical")
ts.add_patterns({
    'preceding_negations': ['abstain from','other than','except for','excluding','lacking','lack of','but','no','not'],
    'following_negations': ['negative','exclusionary']
})
nlp_sz.add_pipe("negex",config={"ent_types":["PROBLEM","TEST","TREATMENT"]})


def chunk_text(text, max_tokens=384):
    words = text.split()
    chunks = []

    while words:
        current_chunk = []
        current_length = 0
        while words and (current_length + len(words[0])) <= max_tokens:
            current_chunk.append(words.pop(0))
            current_length += len(current_chunk[-1])
        chunks.append(' '.join(current_chunk))
    return chunks

def apply(text):
    text = re.sub(r"[^A-Za-z.,:]", " ", text.strip())
    text = re.sub('[.]+', '.', text)
    text = re.sub('[,]+', ',', text)
    text = re.sub(' +', ' ', text)
    text = text.lower()

    chunks = chunk_text(text)
    entities = set()

    for chunk in chunks:
        doc = nlp(chunk)
        entities_chunk = set([ent.text for ent in doc.ents])
        entities = entities.union(entities_chunk)

        nd = nlp_sz(chunk)
        ne = set([ent.text for ent in nd.ents if ent._.negex])

        entities = entities - ne

    if not entities:
        return ["No symptom detected"]
    return list(entities)
