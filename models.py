from transformers import BertModel, BertTokenizer
import torch
from torch import nn
import spacy

RANDOM_SEED = 42
torch.manual_seed(RANDOM_SEED)

class_names = ['negative', 'neutral', 'positive']
PRE_TRAINED_MODEL_NAME = 'bert-base-cased'
tokenizer = BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)

class SentimentClassifier(nn.Module):
    def __init__(self, n_classes):
        super(SentimentClassifier, self).__init__()
        self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
        self.drop = nn.Dropout(p=0.3)
        self.out = nn.Linear(self.bert.config.hidden_size, n_classes)

    def forward(self, input_ids, attention_mask):
        output = self.bert(
        input_ids=input_ids,
        attention_mask=attention_mask
        )
        pooled_output = output[1]
        output = self.drop(pooled_output)
        return self.out(output)

model = SentimentClassifier(len(class_names))

model.load_state_dict(torch.load("BERT Sentiment Analysis/bert_sentiment_analysis.pt", map_location=torch.device('cpu')))

NER = spacy.load("en_core_web_sm", disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"])

def get_sentiment_and_entities(text):
    encoded_review = tokenizer.encode_plus(
        text,
        max_length=512,
        add_special_tokens=True,
        return_token_type_ids=False,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
    )

    input_ids = encoded_review['input_ids']
    attention_mask = encoded_review['attention_mask']

    output = model(input_ids, attention_mask)
    _, prediction = torch.max(output, dim=1)

    # print(f'Review text: {text}')
    # print(f'Sentiment  : {class_names[prediction]}')
    sentiment = prediction.item()

    extracted_entities = NER(text)
    entities = []
    for w in extracted_entities.ents:
        entities.append((w.text, w.label_))

    explained_entities = []
    for e in entities:
        explained_entities.append((e[1], spacy.explain(e[1])))
    explained_entities = list(set(explained_entities))

    return sentiment, entities, explained_entities

print(get_sentiment_and_entities("""The Board of Control for Cricket in India (BCCI) 
                                is the governing body for cricket in India and is under the 
                                jurisdiction of Ministry of Youth Affairs and Sports, Government 
                                of India.[2] The board was formed in December 1928 as a society, 
                                registered under the Tamil Nadu Societies Registration Act. It is 
                                a consortium of state cricket associations and the state associations 
                                select their representatives who in turn elect the BCCI Chief. Its 
                                headquarters are in Wankhede Stadium, Mumbai. Grant Govan was its 
                                first president and Anthony De Mello its first secretary. """))
