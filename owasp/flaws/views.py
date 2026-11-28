from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError, connection
from django.shortcuts import redirect, render

from .models import Account

# for Fix 1, dont forget to import this function
# from django.shortcuts import get_object_or_404

# for fix 2, include this function
# from django.contrib.auth.password_validation import validate_password
# from django.core.exceptions import ValidationError


def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')

    # FLAW 4: A07:2021 – Identification and Authentication Failures
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # FLAW 4 FIX:

        # This enables the validators in AUTH_PASSWORD_VALIDATORS
        # try:
        #     # Passing a temporary User instance lets UserAttributeSimilarityValidator
        #     # check if the password is too similar to the username.
        #     validate_password(password, user=User(username=username))
        # except ValidationError as e:
        #     print(e)
        #     return render(
        #         request,
        #         'flaws/register.html',
        #     )

        try:
            user = User.objects.create_user(
                username=username,
                password=password,  # potentially insecure password without fix
            )
            Account.objects.create(user=user, balance=0)
        except IntegrityError:
            print('Username already taken.')
            return render(
                request,
                'flaws/register.html',
            )

        login(request, user)
        return redirect('/')

    return render(request, 'flaws/register.html')


@login_required
def balanceView(request):
    account_id = request.GET.get('id')

    # FLAW 1: A01:2021 - Broken Access Control (IDOR)
    account = Account.objects.get(id=account_id)

    # FLAW 1 FIX
    # Dont forget import
    # account = get_object_or_404(
    #     Account, id=account_id, user=request.user
    # )

    return render(
        request,
        'flaws/balance.html',
        {'account': account},
    )


@login_required
def addressBookView(request):
    # simplified implementation uses Accounts class

    account_id = request.GET.get('id')
    address_book = []

    # FLAW 3
    with connection.cursor() as cursor:
        cursor.execute(f'SELECT username FROM auth_user WHERE id != "{account_id}"')
        address_book = cursor.fetchall()

    # FLAW 3 FIX
    # slight differences with Account vs sql query, left as improvement
    # address_book = Account.objects.exclude(user_id=request.user.id)

    return render(
        request,
        'flaws/address_book.html',
        {'address_book': address_book},
    )


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
