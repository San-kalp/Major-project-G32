from django.shortcuts import render
from django.http import HttpResponse
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from .forms import searchForm, walletForm , addressForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import TemplateView
from django.views.generic import CreateView #For signing up new user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth.forms import UserCreationForm
from .forms import searchForm, walletForm , addressForm , regexForm 
from django.http import HttpResponseRedirect
import requests
import json
import datetime
import re
from .cryptowallet_risk_scoring.riskreport.client import *
from .cryptowallet_risk_scoring.riskreport.types import *

from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import CreateView #For signing up new user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView , LogoutView
from django.contrib.auth.forms import UserCreationForm

class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'home/sign-up.html'
    success_url="h"

class LogoutInterfaceView(LogoutView):
    template_name = 'home/logout.html'

class LoginInterfaceView(LoginView):
    template_name = 'home/login.html'
    success_url="h"


class lp(TemplateView):
    template_name = 'home/welcome.html'
    extra_context = {'today':datetime.today()}
  

class AuthorisedView(LoginRequiredMixin , TemplateView):
    template_name='home/authorize.html'
    login_url ='/admin'






renderer = JSONRenderer()
ETHERSCAN_API_KEY = "2SFM3DIEINQ9Z7B27U9V4C4ICHUHR25R9A"

regex_patterns = [
        (r'^(bc1)[a-zA-HJ-NP-Z0-9]{25,39}$','Bitcoin Bech 32 Address', range(25,35),'Bitcoin'), #Have to resolve the issue
        (r'^1[a-km-zA-HJ-NP-Z1-9]{25,34}$', 'Bitcoin Legacy (P2PKH) Address', range(25, 35),'Bitcoin'),
        (r'^1\x00([a-km-zA-HJ-NP-Z1-9]\x00){25,34}$', 'Bitcoin Legacy (P2PKH) Address with Null Bytes', range(25, 35),'Bitcoin'),
        (r'^3[a-km-zA-HJ-NP-Z1-9]{25,34}$', 'Bitcoin P2SH Address', range(25, 35),'Bitcoin'),
        (r'^3\x00([a-km-zA-HJ-NP-Z1-9]\x00){25,34}$', 'Bitcoin P2SH Address with Null Bytes', range(25, 35),'Bitcoin'),
        (r'^6P[a-km-zA-HJ-NP-Z1-9]{56}$', 'Bitcoin Private Key (WIF) Compressed', range(56, 57),'Bitcoin'),
        (r'^6\x00P\x00([a-km-zA-HJ-NP-Z1-9]\x00){56}$', 'Bitcoin Private Key (WIF) Compressed with Null Bytes', range(56, 57),'Bitcoin'),
        (r'^5[a-km-zA-HJ-NP-Z1-9]{50}$', 'Bitcoin Private Key (WIF) Uncompressed', range(50, 51),'Bitcoin'),
        (r'^5\x00([a-km-zA-HJ-NP-Z1-9]\x00){50}$', 'Bitcoin Private Key (WIF) Uncompressed with Null Bytes', range(50, 51),'Bitcoin'),
        (r'^[KL][a-km-zA-HJ-NP-Z1-9]{51}$', 'Bitcoin Extended Private Key (xprv) or Extended Public Key (xpub)', range(51, 52),'Bitcoin'),
        (r'^[KL]\x00([a-km-zA-HJ-NP-Z1-9]\x00){51}$', 'Bitcoin Extended Private Key (xprv) or Extended Public Key (xpub) with Null Bytes', range(51, 52),'Bitcoin'),
        (r'^xprv[a-km-zA-HJ-NP-Z1-9]{107,108}$', 'Bitcoin BIP-32 Extended Private Key (xprv)', range(107, 109),'Bitcoin'),
        (r'^xpub[a-km-zA-HJ-NP-Z1-9]{107,108}$', 'Bitcoin BIP-32 Extended Public Key (xpub)', range(107, 109),'Bitcoin'),
        (r'^X[a-km-zA-HJ-NP-Z1-9]{33}$', 'Dash', range(33, 34),'Dash'),
        (r'^D[5-9A-HJ-NP-U][1-9A-HJ-NP-Za-km-z]{32}$', 'Doge', range(34, 35),'Doge'),
        (r'^(L|M|3)[a-km-zA-HJ-NP-Z1-9]{26,33}$', 'Litecoin', range(26, 34),'Litecoin'),
        (r'^r[0-9a-zA-Z]{24,34}$', 'Ripple', range(24, 35),'Ripple'),
        (r'^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$', 'Monero Pattern 1', range(95, 96),'Monero'),
        (r'^[48][0-9AB]|4[1-9A-HJ-NP-Za-km-z]{12}(?:[1-9A-HJ-NP-Za-km-z]{30})?[1-9A-HJ-NP-Za-km-z]{93}$', 'Monero Pattern 2', range(95, 96),'Monero'),
        (r'^0x[a-fA-F0-9]{40}$', 'Ethereum', range(42, 43),'Ethereum')
    ]


def home (request):
    form = searchForm()
    aform = addressForm()
    if request.method =='POST':
        form = searchForm(request.POST)
        aform = addressForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['form_data']
            if len(input_data)>=10 :
                if re.match(r"^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}$",input_data) :
                    url = "https://blockchain.info/rawaddr/%s" %input_data
                    unspent = requests.get('https://blockchain.info/unspent?active=%s' % input_data).json()
                    response = requests.get(url)
                    data = json.loads(response.text)
                    address_ = data["address"]
                    amountReceived = data["total_received"]
                    amountSent = data["total_sent"]
                    balance = data["final_balance"]
                    number_of_transactions = data["n_tx"]
                    transaction = data["txs"]
                    data = wallet_explorer(address=input_data).items()
                    wallet_id = get_wallet_id(address_)
                    context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent, data, wallet_id["wallet_id"]]
                    return render(request,"home/addressInfo.html",{'response':context})
                elif re.match(r"^0x[a-fA-F0-9]{40}$",input_data):
                    string = '{\"eth_addresses\":[\"'+input_data+'\"]}'
                    s1 = json.dumps(string)
                    data = json.loads(s1)
                    report = riskreport_on_entity(**json.loads(data))
                    combined_risk = report.risk_scores.combined_risk
                    reputation_risk = report.risk_scores.reputation_risk

                    # reasons = report.reasons
                    # badneighbors=0
                    # for reason in reasons[1:]:
                    #     print(type(reason.risk_elaboration))
                    #     if(reason.risk_elaboration):
                    #         badneighbors+=reason.get('riskElaboration').get("howManyBadRecipients")

                    # print("jdijsisijs .......................................", badneighbors)
                    
                    # print(json.dumps(report.as_json()))
                    # print(report)
                    with open('risk_node_data.json', 'w', encoding='utf-8') as f:
                        json.dump(report.as_json(), f, ensure_ascii=False, indent=4)
                    
                    node_color = 0
                    if(combined_risk<=35):
                        node_color = 0
                    elif (combined_risk>35 and combined_risk<60):
                        node_color = 1
                    else:
                        node_color = 2
                    context = [input_data, report.risk_scores.combined_risk, report.risk_scores.reputation_risk, report.risk_scores.fraud_risk, report.risk_scores.lending_risk, node_color]
                    # print(context)

                    return render(request,"home/riskscore.html",{'response':context})
                else :
                    context = get_tx_data(input_data)
                    return render(request,"home/transactionInfo.html",{'response':context})
            else :
                query = f"http://www.walletexplorer.com/api/1/firstbits?prefix={input_data}&caller=sankalp.chordia20@vit.edu"
                response = requests.get(query)
                address = json.loads(response.text)["address"]
                print(address)
                url = "https://blockchain.info/rawaddr/%s" %address
                unspent = requests.get('https://blockchain.info/unspent?active=%s' % address).json()
                response = requests.get(url)
                data = json.loads(response.text)
                address_ = data["address"]
                amountReceived = data["total_received"]
                amountSent = data["total_sent"]
                balance = data["final_balance"]
                number_of_transactions = data["n_tx"]
                transaction = data["txs"]
                data = wallet_explorer(address=input_data).items()
                wallet_id = get_wallet_id(address_)
                context = [address_,amountReceived,amountSent,balance,number_of_transactions,transaction,unspent, data, wallet_id["wallet_id"]]
                return render(request,"home/addressInfo.html",{'response':context})
            

        if aform.is_valid():
            address = aform.cleaned_data['address']
            for pattern, pattern_name, length_range in regex_patterns:
                 if re.match(pattern, address) and len(address) in length_range:
                     print(pattern, "\t" , pattern_name)

        


                        



    context = {'form':form,'aform':aform}
    return render(request,"home/home.html",context=context)



def wallet_explorer(address):
    query = f"http://www.walletexplorer.com/api/1/address-lookup?address={address}&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)


def get_tx_data(txid):
    query = f"http://www.walletexplorer.com/api/1/tx?txid={txid}&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)

def get_wallet_id(address):
    query = f"http://www.walletexplorer.com/api/1/address?address={address}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    return json.loads(requests.get(query).text)


def wallet(request):
    form = walletForm()
    context={'form':form}
    return render(request,"home/wallet.html",context=context)

def wallet_detail(request, wallet):
    query = f"http://www.walletexplorer.com/api/1/wallet-addresses?wallet={wallet}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    data = json.loads(requests.get(query).text)
    return render(request,"home/wallet_detail.html",{'response':data})

def wallet_transactions(request, wallet):
    query = f"http://www.walletexplorer.com/api/1/wallet?wallet={wallet}&from=0&count=100&caller=sankalp.chordia20@vit.edu"
    data = json.loads(requests.get(query).text)
    return render(request,"home/wallet_detail_transactions.html",{'response':data})

def blogs(request):
    return render(request, "home/blogs.html")

def qrcode(request):
     return render(request, "home/qrcode.html")

def regex(request):
    desc=""
    cryptocurrency=""
    form = regexForm()
    if request.method == 'POST':
        form = regexForm(request.POST)
        if form.is_valid():
            input_data = form.cleaned_data['regex']
            for regex, description, length_range , crypto in regex_patterns:
                if re.match(regex, input_data):
                    matched_length = len(input_data)
                    if matched_length in length_range:
                        desc = description
                        cryptocurrency = crypto
                        break
    context = {'form':form,'desc':desc,'cryptocurrency':cryptocurrency}
    return render(request, "home/regex.html",context=context)


