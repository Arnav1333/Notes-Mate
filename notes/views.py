from django.shortcuts import render,redirect, get_object_or_404
from .models import Note
from .forms import NoteForm
import fitz 
from transformers import pipeline
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
import pytz
from django.contrib.auth.decorators import login_required

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

@login_required
def upload_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False) 
            note.user = request.user
            note.save()         
            note.extracted_text = extract_text_from_pdf(note.pdf_file.path)
            note.summary = generate_summary(note.extracted_text)
            
            note.save() 
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'upload_note.html', {'form': form})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    ist = pytz.timezone('Asia/Kolkata')
    for note in notes:
        note.uploaded_at = note.uploaded_at.astimezone(ist) 
    return render(request,'note_list.html', {'notes': notes})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id,user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'confirm_delete.html', {'note': note})


def register(request):
    if request.method == "POST":
        form  = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')