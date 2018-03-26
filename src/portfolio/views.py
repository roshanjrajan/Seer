from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Transaction

# Create your views here.
class port_view(TemplateView):
	template_name = 'portfolio/home.html'


class TransactionListView(ListView):
    model = Transaction

class TransactionDetailView(UpdateView):
    model = Transaction
    fields = '__all__'
    success_url = "/portfolio/txn"

class TransactionCreateView(CreateView):
    model = Transaction
    fields = '__all__'
    success_url = "/portfolio/txn"


class TransactionDeleteView(DeleteView):
    model = Transaction
    fields = '__all__'
    success_url = "/portfolio/txn"

