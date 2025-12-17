"""
Named Entity Recognition (NER) System
Advanced NLP-based entity extraction and classification
Extracts: PERSON, ORGANIZATION, LOCATION, DATE, MONEY, etc.
"""

import re
import spacy
from collections import Counter, defaultdict
import json
from datetime import datetime

class EntityRecognitionSystem:
    def __init__(self, model='en_core_web_sm'):
        """
        Initialize NER system with spaCy
        Models available: en_core_web_sm, en_core_web_md, en_core_web_lg
        """
        try:
            self.nlp = spacy.load(model)
        except OSError:
            print(f"Model {model} not found. Downloading...")
            import os
            os.system(f'python -m spacy download {model}')
            self.nlp = spacy.load(model)
        
        self.entity_types = {
            'PERSON': 'People, including fictional',
            'NORP': 'Nationalities or religious or political groups',
            'FAC': 'Buildings, airports, highways, bridges, etc.',
            'ORG': 'Companies, agencies, institutions, etc.',
            'GPE': 'Countries, cities, states',
            'LOC': 'Non-GPE locations, mountain ranges, bodies of water',
            'PRODUCT': 'Objects, vehicles, foods, etc.',
            'EVENT': 'Named hurricanes, battles, wars, sports events, etc.',
            'WORK_OF_ART': 'Titles of books, songs, etc.',
            'LAW': 'Named documents made into laws',
            'LANGUAGE': 'Any named language',
            'DATE': 'Absolute or relative dates or periods',
            'TIME': 'Times smaller than a day',
            'PERCENT': 'Percentage, including "%"',
            'MONEY': 'Monetary values, including unit',
            'QUANTITY': 'Measurements, as of weight or distance',
            'ORDINAL': '"first", "second", etc.',
            'CARDINAL': 'Numerals that do not fall under another type'
        }
    
    def extract_entities(self, text):
        """Extract all named entities from text"""
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char,
                'description': self.entity_types.get(ent.label_, 'Unknown entity type')
            })
        
        return entities
    
    def extract_by_type(self, text, entity_type):
        """Extract entities of a specific type"""
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents if ent.label_ == entity_type]
        return list(set(entities))  # Remove duplicates
    
    def get_people(self, text):
        """Extract all person names"""
        return self.extract_by_type(text, 'PERSON')
    
    def get_organizations(self, text):
        """Extract all organization names"""
        return self.extract_by_type(text, 'ORG')
    
    def get_locations(self, text):
        """Extract all locations (GPE and LOC)"""
        doc = self.nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ in ['GPE', 'LOC']]
        return list(set(locations))
    
    def get_dates(self, text):
        """Extract all dates and time references"""
        return self.extract_by_type(text, 'DATE')
    
    def get_money(self, text):
        """Extract all monetary values"""
        return self.extract_by_type(text, 'MONEY')
    
    def analyze_text(self, text):
        """Complete entity analysis of text"""
        doc = self.nlp(text)
        
        # Extract entities by type
        entities_by_type = defaultdict(list)
        for ent in doc.ents:
            entities_by_type[ent.label_].append(ent.text)
        
        # Count entity occurrences
        entity_counts = Counter([ent.label_ for ent in doc.ents])
        
        # Get most common entities
        all_entities = [ent.text for ent in doc.ents]
        most_common = Counter(all_entities).most_common(10)
        
        return {
            'total_entities': len(doc.ents),
            'entity_counts': dict(entity_counts),
            'entities_by_type': dict(entities_by_type),
            'most_common_entities': most_common,
            'entity_types_found': list(entity_counts.keys())
        }
    
    def extract_relationships(self, text):
        """Extract subject-verb-object relationships"""
        doc = self.nlp(text)
        relationships = []
        
        for sent in doc.sents:
            for token in sent:
                if token.dep_ == 'ROOT':
                    subject = [child for child in token.children if child.dep_ in ['nsubj', 'nsubjpass']]
                    obj = [child for child in token.children if child.dep_ in ['dobj', 'pobj']]
                    
                    if subject and obj:
                        relationships.append({
                            'subject': subject[0].text,
                            'verb': token.text,
                            'object': obj[0].text
                        })
        
        return relationships
    
    def extract_noun_phrases(self, text):
        """Extract all noun phrases"""
        doc = self.nlp(text)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        return noun_phrases
    
    def visualize_entities(self, text):
        """Create HTML visualization of entities"""
        doc = self.nlp(text)
        
        html_parts = []
        last_end = 0
        
        colors = {
            'PERSON': '#aa9cfc',
            'ORG': '#7aecec',
            'GPE': '#feca74',
            'LOC': '#ff9561',
            'DATE': '#bfe1d9',
            'MONEY': '#e4e7d2',
            'PRODUCT': '#ffeb80'
        }
        
        for ent in doc.ents:
            # Add text before entity
            html_parts.append(text[last_end:ent.start_char])
            
            # Add entity with color
            color = colors.get(ent.label_, '#ddd')
            html_parts.append(
                f'<mark style="background-color: {color}; padding: 0.2em 0.3em; '
                f'border-radius: 0.25em; line-height: 2;">'
                f'{ent.text} <span style="font-size: 0.8em; font-weight: bold; '
                f'line-height: 1; border-radius: 0.35em; text-transform: uppercase; '
                f'vertical-align: middle; margin-left: 0.5em">{ent.label_}</span></mark>'
            )
            
            last_end = ent.end_char
        
        # Add remaining text
        html_parts.append(text[last_end:])
        
        return ''.join(html_parts)
    
    def extract_custom_patterns(self, text, pattern_dict):
        r"""
        Extract entities based on custom regex patterns
        pattern_dict: {'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', ...}
        """
        custom_entities = defaultdict(list)
        
        for entity_type, pattern in pattern_dict.items():
            matches = re.findall(pattern, text)
            custom_entities[entity_type].extend(matches)
        
        return dict(custom_entities)
    
    def batch_process(self, texts):
        """Process multiple texts efficiently"""
        results = []
        
        for doc in self.nlp.pipe(texts):
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_
                })
            results.append(entities)
        
        return results
    
    def export_entities(self, text, format='json'):
        """Export entities in different formats"""
        entities = self.extract_entities(text)
        
        if format == 'json':
            return json.dumps(entities, indent=2)
        elif format == 'csv':
            lines = ['text,label,start,end,description']
            for ent in entities:
                lines.append(f'"{ent["text"]}",{ent["label"]},{ent["start"]},{ent["end"]},"{ent["description"]}"')
            return '\n'.join(lines)
        else:
            return entities
    
    def get_entity_context(self, text, entity_text, window=50):
        """Get context around a specific entity"""
        doc = self.nlp(text)
        contexts = []
        
        for ent in doc.ents:
            if ent.text == entity_text:
                start = max(0, ent.start_char - window)
                end = min(len(text), ent.end_char + window)
                context = text[start:end]
                contexts.append(context)
        
        return contexts


# Advanced NER Features
class AdvancedEntityExtractor(EntityRecognitionSystem):
    """Extended NER with custom entity recognition"""
    
    def __init__(self):
        super().__init__()
        
        # Custom patterns for additional entities
        self.custom_patterns = {
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'URL': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'IP_ADDRESS': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
            'CREDIT_CARD': r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',
            'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
            'HASHTAG': r'#\w+',
            'MENTION': r'@\w+'
        }
    
    def extract_all(self, text):
        """Extract both spaCy entities and custom patterns"""
        # Get spaCy entities
        spacy_entities = self.extract_entities(text)
        
        # Get custom pattern entities
        custom_entities = self.extract_custom_patterns(text, self.custom_patterns)
        
        return {
            'standard_entities': spacy_entities,
            'custom_entities': custom_entities
        }
    
    def anonymize_text(self, text, entity_types=None):
        """Replace entities with placeholders for privacy"""
        if entity_types is None:
            entity_types = ['PERSON', 'ORG', 'GPE', 'DATE']
        
        doc = self.nlp(text)
        anonymized = text
        
        # Sort entities by position (reverse to maintain indices)
        entities = sorted(doc.ents, key=lambda x: x.start_char, reverse=True)
        
        for ent in entities:
            if ent.label_ in entity_types:
                placeholder = f'[{ent.label_}]'
                anonymized = anonymized[:ent.start_char] + placeholder + anonymized[ent.end_char:]
        
        return anonymized
    
    def entity_linking(self, text):
        """Link entities to Wikipedia (simple implementation)"""
        entities = self.extract_entities(text)
        
        for entity in entities:
            if entity['label'] in ['PERSON', 'ORG', 'GPE']:
                # Create Wikipedia link
                wiki_name = entity['text'].replace(' ', '_')
                entity['wiki_url'] = f'https://en.wikipedia.org/wiki/{wiki_name}'
        
        return entities


# Example usage and testing
if __name__ == "__main__":
    print("="*70)
    print("NAMED ENTITY RECOGNITION SYSTEM")
    print("="*70)
    
    # Sample text
    sample_text = """
    Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 
    Cupertino, California on April 1, 1976. The company is currently valued at 
    over $2.5 trillion. Tim Cook became CEO in 2011 after Steve Jobs passed away.
    Apple's headquarters, Apple Park, opened in 2017 in Silicon Valley.
    
    Contact: info@apple.com or call 1-800-MY-APPLE.
    Visit us at https://www.apple.com
    """
    
    # Initialize system
    print("\n1. Initializing NER System...")
    ner = AdvancedEntityExtractor()
    
    # Extract all entities
    print("\n2. Extracting Entities...")
    entities = ner.extract_entities(sample_text)
    print(f"\nFound {len(entities)} entities:")
    for ent in entities[:10]:
        print(f"  - {ent['text']:30} [{ent['label']}]")
    
    # Get specific entity types
    print("\n3. Extracting Specific Types...")
    people = ner.get_people(sample_text)
    print(f"\nPeople: {people}")
    
    orgs = ner.get_organizations(sample_text)
    print(f"Organizations: {orgs}")
    
    locations = ner.get_locations(sample_text)
    print(f"Locations: {locations}")
    
    dates = ner.get_dates(sample_text)
    print(f"Dates: {dates}")
    
    money = ner.get_money(sample_text)
    print(f"Money: {money}")
    
    # Analyze text
    print("\n4. Complete Analysis...")
    analysis = ner.analyze_text(sample_text)
    print(f"\nTotal Entities: {analysis['total_entities']}")
    print(f"Entity Types Found: {analysis['entity_types_found']}")
    print(f"\nEntity Counts:")
    for entity_type, count in analysis['entity_counts'].items():
        print(f"  {entity_type}: {count}")
    
    # Extract custom patterns
    print("\n5. Extracting Custom Patterns...")
    all_entities = ner.extract_all(sample_text)
    print(f"\nCustom Entities Found:")
    for entity_type, values in all_entities['custom_entities'].items():
        if values:
            print(f"  {entity_type}: {values}")
    
    # Anonymize text
    print("\n6. Anonymizing Text...")
    anonymized = ner.anonymize_text(sample_text, ['PERSON', 'ORG', 'DATE'])
    print(f"\nAnonymized Text:")
    print(anonymized[:200] + "...")
    
    # Export entities
    print("\n7. Exporting Entities...")
    json_export = ner.export_entities(sample_text, format='json')
    print(f"\nJSON Export (first 300 chars):")
    print(json_export[:300] + "...")
    
    print("\n" + "="*70)
    print("NER System Demo Complete!")
    print("="*70)