from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json
from .models import Document
from rules.models import Rule
from rules.rule_checker import apply_rules


def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/list.html', {
        'documents': documents
    })


def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    mode = request.GET.get('mode', 'write')
    
    rules = Rule.objects.all()
    rules_json = json.dumps([{
        'id': rule.id,
        'name': rule.name,
        'rule_type': rule.rule_type,
        'is_active': rule.is_active
    } for rule in rules])
    
    return render(request, 'documents/detail.html', {
        'document': document,
        'mode': mode,
        'settings_json': json.dumps(document.settings),
        'rules_json': rules_json
    })


def document_create(request):
    if request.method == 'POST':
        title = request.POST.get('title', 'Untitled')
        document = Document.objects.create(title=title)
        return redirect('document_detail', pk=document.pk)
    return redirect('document_list')


@require_http_methods(["POST"])
def document_autosave(request, pk):
    document = get_object_or_404(Document, pk=pk)
    data = json.loads(request.body)
    
    if 'content' in data:
        document.content = data['content']
    if 'notes' in data:
        document.notes = data['notes']
    if 'title' in data:
        document.title = data['title']
    
    document.save()
    
    return JsonResponse({
        'status': 'success',
        'updated_at': document.updated_at.isoformat()
    })





def document_export(request, pk):
    document = get_object_or_404(Document, pk=pk)
    format_type = request.GET.get('format', 'markdown')
    
    if format_type == 'markdown':
        response = HttpResponse(document.content, content_type='text/markdown')
        response['Content-Disposition'] = f'attachment; filename="{document.title}.md"'
        return response
    
    
    return JsonResponse({'error': 'Invalid format'}, status=400)


@require_http_methods(["POST"])
def document_check_rules(request, pk):
    document = get_object_or_404(Document, pk=pk)
    data = json.loads(request.body)
    
    text = data.get('text', document.content)
    active_rule_ids = data.get('rule_ids', [])
    
    active_rules = []
    if active_rule_ids:
        rules = Rule.objects.filter(id__in=active_rule_ids, is_active=True)
    else:
        rules = Rule.objects.filter(is_active=True)
    
    for rule in rules:
        active_rules.append({
            'name': rule.name,
            'rule_type': rule.rule_type,
            'pattern': rule.pattern
        })
    
    matches = apply_rules(text, active_rules)
    
    return JsonResponse({
        'matches': matches
    })


@require_http_methods(["POST", "DELETE"])
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    return JsonResponse({'status': 'success'})




@require_http_methods(["POST"])
def document_generate_share(request, pk):
    document = get_object_or_404(Document, pk=pk)
    token = document.generate_share_token()
    share_url = request.build_absolute_uri(f'/share/{token}/')
    return JsonResponse({
        'status': 'success',
        'token': token,
        'url': share_url
    })


def document_share_view(request, token):
    document = get_object_or_404(Document, share_token=token)
    mode = request.GET.get('mode', 'write')
    
    rules = Rule.objects.all()
    rules_json = json.dumps([{
        'id': rule.id,
        'name': rule.name,
        'rule_type': rule.rule_type,
        'is_active': rule.is_active
    } for rule in rules])
    
    return render(request, 'documents/detail.html', {
        'document': document,
        'mode': mode,
        'settings_json': json.dumps(document.settings),
        'rules_json': rules_json,
        'is_shared': True
    })
