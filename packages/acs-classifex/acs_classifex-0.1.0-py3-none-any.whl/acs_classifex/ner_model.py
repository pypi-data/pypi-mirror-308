import spacy
from spacy.tokens import DocBin

def train_ner(training_data, model_name='acs_classifex'):
    """
    Train a custom NER model using spaCy.
    
    Args:
        training_data (list): A list of training examples in the format 
                              [(text, {'entities': [(start, end, label)]}), ...]
        model_name (str): Name for the saved model.
    """
    # Load a blank SpaCy model
    nlp = spacy.blank("en")

    # Add NER to the pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner")

    # Add labels to the NER
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # Prepare training data
    db = DocBin()
    for text, annotations in training_data:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annotations.get("entities"):
            span = doc.char_span(start, end, label=label)
            if span:
                ents.append(span)
        doc.ents = ents
        db.add(doc)

    # Begin training
    nlp.begin_training()
    for iteration in range(10):  # Number of training iterations
        for batch in spacy.util.minibatch(training_data, size=2):
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = spacy.training.Example.from_dict(doc, annotations)
                nlp.update([example])

    # Save the model
    nlp.to_disk(model_name)
    print(f"Model saved to {model_name}")

def load_model(model_name='acs_classifex'):
    """
    Load the trained custom NER model.
    
    Args:
        model_name (str): Name of the saved model directory.
    Returns:
        nlp: Loaded spaCy model
    """
    nlp = spacy.load(model_name)
    return nlp
