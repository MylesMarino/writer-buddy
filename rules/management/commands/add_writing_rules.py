from django.core.management.base import BaseCommand
from rules.models import Rule


class Command(BaseCommand):
    help = 'Add comprehensive writing rules'

    def handle(self, *args, **options):
        rules_data = [
            {
                'name': 'Remove -ly adverbs',
                'rule_type': 'preset',
                'description': 'Highlights adverbs ending in -ly',
                'is_active': True,
                'pattern': r'\b\w+ly\b'
            },
            {
                'name': 'Remove: just',
                'rule_type': 'preset',
                'description': 'Remove the word "just"',
                'is_active': True,
                'pattern': r'\bjust\b'
            },
            {
                'name': 'Remove: that',
                'rule_type': 'preset',
                'description': 'Remove the word "that"',
                'is_active': True,
                'pattern': r'\bthat\b'
            },
            {
                'name': 'Remove: then',
                'rule_type': 'preset',
                'description': 'Remove the word "then"',
                'is_active': True,
                'pattern': r'\bthen\b'
            },
            {
                'name': 'Remove: very',
                'rule_type': 'preset',
                'description': 'Remove the word "very"',
                'is_active': True,
                'pattern': r'\bvery\b'
            },
            {
                'name': 'Remove: start/begin',
                'rule_type': 'preset',
                'description': 'Remove start, begin, began, begun',
                'is_active': True,
                'pattern': r'\b(start|begin|began|begun)\b'
            },
            {
                'name': 'Remove: rather',
                'rule_type': 'preset',
                'description': 'Remove the word "rather"',
                'is_active': True,
                'pattern': r'\brather\b'
            },
            {
                'name': 'Remove: quite',
                'rule_type': 'preset',
                'description': 'Remove the word "quite"',
                'is_active': True,
                'pattern': r'\bquite\b'
            },
            {
                'name': 'Remove: sort of',
                'rule_type': 'preset',
                'description': 'Remove "sort of"',
                'is_active': True,
                'pattern': r'\bsort of\b'
            },
            {
                'name': 'Remove: a little',
                'rule_type': 'preset',
                'description': 'Remove "a little"',
                'is_active': True,
                'pattern': r'\ba little\b'
            },
            {
                'name': 'Use words not numbers',
                'rule_type': 'preset',
                'description': 'Use five not 5',
                'is_active': True,
                'pattern': r'\b\d+\b'
            },
            {
                'name': 'Speaker tags - avoid fancy',
                'rule_type': 'custom',
                'description': 'Check for speaker tags that aren\'t said/says/asked/asks',
                'is_active': False,
                'pattern': r'"[^"]*"\s+(whispered|shouted|screamed|yelled|exclaimed|declared|announced|replied|responded|muttered|murmured)'
            },
            {
                'name': 'Passive voice detection',
                'rule_type': 'preset',
                'description': 'Detects passive voice constructions',
                'is_active': True,
                'pattern': ''
            },
            {
                'name': 'Repeated words',
                'rule_type': 'preset',
                'description': 'Finds repeated words',
                'is_active': True,
                'pattern': ''
            },
            {
                'name': 'Long sentences',
                'rule_type': 'preset',
                'description': 'Flags sentences longer than 30 words',
                'is_active': True,
                'pattern': ''
            },
        ]

        for rule_data in rules_data:
            rule, created = Rule.objects.get_or_create(
                name=rule_data['name'],
                defaults=rule_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created rule: {rule.name}'))
            else:
                for key, value in rule_data.items():
                    setattr(rule, key, value)
                rule.save()
                self.stdout.write(f'Updated rule: {rule.name}')
