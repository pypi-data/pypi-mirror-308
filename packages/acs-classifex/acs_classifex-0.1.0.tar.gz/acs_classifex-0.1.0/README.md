# acs_classifex

This package provides utilities to train and load a custom Named Entity Recognition (NER) model using spaCy.

## Installation

```bash
pip install acs_classifex
```

## Usage

from acs_classifex import train_ner, load_model

# Training data format: [(text, {'entities': [(start, end, label)]})]

training_data = [
("Apple is looking at buying U.K. startup for $1 billion", {'entities': [(0, 5, 'ORG'), (27, 31, 'GPE'), (44, 54, 'MONEY')]}),
("San Francisco is a beautiful city", {'entities': [(0, 13, 'GPE')]})
]

# Train the NER model

train_ner(training_data)

# Load the trained model

nlp = load*model()
doc = nlp("Apple is acquiring a company in London")
print([(ent.text, ent.label*) for ent in doc.ents])
