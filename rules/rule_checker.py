import re


class RuleChecker:
    
    @staticmethod
    def check_word_filter(text, pattern):
        matches = []
        for match in re.finditer(r'\b' + re.escape(pattern) + r'\b', text, re.IGNORECASE):
            matches.append({
                'start': match.start(),
                'end': match.end(),
                'text': match.group(),
                'suggestion': f'Consider removing "{match.group()}"'
            })
        return matches
    
    @staticmethod
    def check_passive_voice(text):
        matches = []
        passive_patterns = [
            r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',
            r'\b(is|are|was|were|be|been|being)\s+\w+en\b',
        ]
        
        for pattern in passive_patterns:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group(),
                    'suggestion': 'Consider using active voice'
                })
        return matches
    
    @staticmethod
    def check_repeated_words(text):
        matches = []
        pattern = r'\b(\w+)\s+\1\b'
        
        for match in re.finditer(pattern, text, re.IGNORECASE):
            matches.append({
                'start': match.start(),
                'end': match.end(),
                'text': match.group(),
                'suggestion': f'Repeated word: "{match.group(1)}"'
            })
        return matches
    
    @staticmethod
    def check_sentence_length(text):
        matches = []
        sentences = re.split(r'[.!?]+', text)
        position = 0
        
        for sentence in sentences:
            if sentence.strip():
                word_count = len(sentence.split())
                if word_count > 30:
                    matches.append({
                        'start': position,
                        'end': position + len(sentence),
                        'text': sentence.strip(),
                        'suggestion': f'Long sentence ({word_count} words). Consider breaking it up.'
                    })
            position += len(sentence) + 1
        
        return matches
    
    @staticmethod
    def check_custom_pattern(text, pattern):
        matches = []
        try:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                matches.append({
                    'start': match.start(),
                    'end': match.end(),
                    'text': match.group(),
                    'suggestion': 'Custom rule match'
                })
        except re.error:
            pass
        
        return matches


def apply_rules(text, active_rules):
    all_matches = []
    
    for rule in active_rules:
        matches = []
        
        if rule['rule_type'] == 'preset':
            rule_name = rule['name']
            
            if rule_name == 'Passive voice detection':
                matches = RuleChecker.check_passive_voice(text)
            elif rule_name == 'Repeated words':
                matches = RuleChecker.check_repeated_words(text)
            elif rule_name == 'Long sentences':
                matches = RuleChecker.check_sentence_length(text)
            elif 'Remove:' in rule_name or rule_name.startswith('Remove -ly'):
                if rule_name == 'Remove -ly adverbs' and rule.get('pattern'):
                    matches = RuleChecker.check_custom_pattern(text, rule['pattern'])
                    for match in matches:
                        match['suggestion'] = f'Consider removing adverb "{match["text"]}"'
                elif rule.get('pattern'):
                    matches = RuleChecker.check_custom_pattern(text, rule['pattern'])
                    for match in matches:
                        match['suggestion'] = f'Consider removing "{match["text"]}"'
            elif 'Use words not numbers' in rule_name and rule.get('pattern'):
                matches = RuleChecker.check_custom_pattern(text, rule['pattern'])
                for match in matches:
                    match['suggestion'] = f'Spell out "{match["text"]}" as a word'
            elif rule.get('pattern'):
                matches = RuleChecker.check_custom_pattern(text, rule['pattern'])
        elif rule['rule_type'] == 'custom' and rule.get('pattern'):
            matches = RuleChecker.check_custom_pattern(text, rule['pattern'])
        
        for match in matches:
            if 'suggestion' not in match:
                match['suggestion'] = 'Consider revising'
            match['rule_name'] = rule['name']
            all_matches.append(match)
    
    all_matches.sort(key=lambda x: x['start'])
    
    return all_matches
