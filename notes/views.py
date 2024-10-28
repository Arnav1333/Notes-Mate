from django.shortcuts import render,redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
import fitz 
from transformers import pipeline

# Create your views here.

summarization_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def home(request):
    return render(request,'home.html')

def extract_text_from_pdf(pdf_path):
   
    with fitz.open(pdf_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text


def generate_summary(text):
    max_length = 2024  
    truncated_text = text[:max_length]  
    summary = summarization_pipeline(truncated_text)  
    return summary


def upload_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False) 
            note.save()         
            note.extracted_text = extract_text_from_pdf(note.pdf_file.path)
            note.summary = generate_summary(note.extracted_text)
            
            note.save() 
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'upload_note.html', {'form': form})

def note_list(request):
    notes = Note.objects.all()
    return render(request,'note_list.html', {'notes': notes})

def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'confirm_delete.html', {'note': note})


