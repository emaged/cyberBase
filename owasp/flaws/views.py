from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Account


@login_required
def transferView(request):

    if request.method == 'POST':
        to = User.objects.get(username=request.POST.get('to'))
        amount = int(request.POST.get('amount'))

        toAccount = Account.objects.get(user_id=to.id)
        fromAccount = Account.objects.get(user_id=request.user.id)

        if not toAccount or not fromAccount:
            redirect('/')

        if fromAccount.balance < amount:
            redirect('/')

        # should be transaction
        fromAccount.balance -= amount
        toAccount.balance += amount

        fromAccount.save()
        toAccount.save()

    return redirect('/')


@login_required
def homePageView(request):
    accounts = Account.objects.exclude(user_id=request.user.id)
    return render(request, 'flaws/index.html', {'accounts': accounts})


# Create your views here.
