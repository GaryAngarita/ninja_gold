from django.shortcuts import render, redirect
import random
from time import gmtime, strftime
import tkinter
from tkinter import messagebox

location = {
    'farm': random.randint(10, 20),
    'cave': random.randint(5, 10),
    'house': random.randint(2, 5),
    'casino': random.randint(-50, 50)
}


def index(request):
    
    #context = {
        #'farm': random.randint(10, 20),
        #'cave': random.randint(5, 10),
        #'house': random.randint(2, 5),
        #'casino': random.randint(-50, 50)
    #}
    if 'gold' not in request.session or 'activities' not in request.session:
        request.session['gold'] = 0
        request.session['activities'] = []
    context = {
        "activities": request.session['activities']
    }
    return render(request, "ninja.html", context)

def process_money(request):   
    if request.method == 'POST':
        myGold = request.session['gold']
        location = request.POST['location']
        myTime = strftime("%B %d, %Y %H:%M %p", gmtime())
        activities = request.session['activities']
        if location == 'farm':
            goldThisTurn = round(random.random() * 10 + 10)
            
        elif location == 'cave':
            goldThisTurn = round(random.random() * 5 + 5)
            
        elif location == 'house':
            goldThisTurn = round(random.randint(2, 5))
            
        else:
            goldThisTurn = round(random.randint(-50, 50))
        myGold += goldThisTurn
        request.session['gold'] = myGold
        if goldThisTurn < 0:
            str = f'{len(activities) + 1}. Lost {abs(goldThisTurn)} gold from the {location}! Feeling lucky? {myTime}'
        else:
            str = f'{len(activities) + 1}. Earned {goldThisTurn} gold from the {location}! Lucky you! {myTime}'
        activities.insert(0, str)
        request.session['activities'] = activities        
    if myGold >= 250:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Congratulations!", f'You made {myGold} gold!')
        return redirect('/reset')
    elif len(request.session['activities']) == 20 and myGold < 250:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Sorry!", f"You only earned {myGold} gold")
        return redirect('/reset')
    return redirect('/')

def reset_game(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
