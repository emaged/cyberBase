from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .models import Account

# for Fix 1, dont forget to import this function
# from django.shortcuts import get_object_or_404


@login_required
def balanceView(request):
    account_id = request.GET.get('id')

    # FLAW 1: A01:2021 - Broken Access Control (IDOR)
    account = Account.objects.get(id=account_id)

    # FLAW 1 FIX
    # account = get_object_or_404(
    #     Account, id=account_id, user=request.user
    # )

    return render(request, 'flaws/balance.html', {'account': account})


@login_required
def transferView(request):

    if request.method == 'POST':
        to = User.objects.get(username=request.POST.get('to'))
        amount = int(request.POST.get('amount'))

        toAccount = Account.objects.get(user_id=to.id)
        fromAccount = Account.objects.get(user_id=request.user.id)

        if amount < 0:
            return redirect('/')

        if not toAccount or not fromAccount:
            return redirect('/')

        if fromAccount.balance < amount:
            return redirect('/')

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
