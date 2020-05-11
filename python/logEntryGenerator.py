#######################################
# wichtig: ich muss dran denken,      #
# dass die einträge nicht gleichmäßig #
# zufällig verteilt sind              #
#######################################

import datetime
import random
import argparse
import string
import os
from time import sleep

widgets = [
    "Incoming request: GET /MULTIVERSA-IFP/core/pao/web/paymententry/payment_entry_detail.jsf?screenType=CREDIT_TRANSFER&widgetAction=MORE_DETAILS&directAccess=True&widget=paymentEntry&localAccountId=&beneficiaryId=&currency=EUR&amount=&remittanceInformation= userAgent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36] device=COMPUTER processingTime=186",
    "Incoming request: GET /MULTIVERSA-IFP/core/pao/open_payments.jsf?selectedView=pao.guiList.view.toBeAuthorisedByMe&paymentType=1&widget=summary userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=65",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.intradayReportsView&viewType=0&widget=balancesColumn userAgent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36] device=COMPUTER processingTime=329",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/accountGroups/liquidity_account_groups.jsf?selectedView=ecm.liquidity.accountGroups.view.all&viewType=0&widget=LiquidityByAccountGroupsWidgetContent userAgent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36] device=COMPUTER processingTime=42",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.intradayReportsView&viewType=0&widget=favouriteViews userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/currencies/liquidity_currencies.jsf?selectedView=ecm.liquidity.currencies.view.all&viewType=0&widget=LiquidityByCurrenciesWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.intradayReportsView&viewType=0&widget=balancesByCurrencies userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/transaction/transactions_overview.jsf?selectedView=ecm.reporting.transactions.mainList.view.allTransactionsMainListReport&viewType=0&widget=IncomingTransactionsWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=48",
    "Incoming request: GET /MULTIVERSA-IFP/core/pao/open_payments.jsf?selectedView=pao.guiList.view.allPayments&widget=openPayments userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.allAccountsView&viewType=0&widget=BalancesListWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=50",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/accounts/liquidity_accounts.jsf?selectedView=ecm.liquidity.accounts.view.all&viewType=0&widget=LiquidityByAccountsWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=57",
    "Incoming request: GET /MULTIVERSA-IFP/core/pao/transmitted_payments.jsf?selectedView=pao.guiList.view.completed&viewType=0&widget=TransmittedPaymentsWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=66",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/transaction/transactions_overview.jsf?selectedView=ecm.reporting.transactions.mainList.view.allTransactionsMainListReport&viewType=0&widget=transactionByDate userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=55",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/banks/liquidity_banks.jsf?selectedView=ecm.liquidity.banks.view.all&viewType=0&widget=LiquidityByBanksWidgetContent&banks=RpBLVhy85c5u4nGKeISH0A userAgent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36] device=COMPUTER processingTime=51",
    "Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/countries/liquidity_countries.jsf?selectedView=ecm.liquidity.countries.view.all&viewType=0&widget=LiquidityByCountriesWidgetContent&countries=NL userAgent=[Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36] device=COMPUTER processingTime=54"]


def fixedRoutine(logFile, sessionid):
    elements = []
    #elements = [4,10,6]
    elements.append("Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.intradayReportsView&viewType=0&widget=favouriteViews userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54")
    elements.append("Incoming request: GET /MULTIVERSA-IFP/lightning/ecm/liquidity/accounts/liquidity_accounts.jsf?selectedView=ecm.liquidity.accounts.view.all&viewType=0&widget=LiquidityByAccountsWidgetContent userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=57")
    elements.append("Incoming request: GET /MULTIVERSA-IFP/lightning/reporting/balance/balance_overview.jsf?selectedView=ecm.reporting.balance.overview.intradayReportsView&viewType=0&widget=balancesByCurrencies userAgent=[Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0] device=COMPUTER processingTime=54")
    print(args.fixedRoutine)
    if isinstance(args.fixedRoutine,str):
        args.fixedRoutine = args.fixedRoutine.split(',')
    for i in args.fixedRoutine:
        sleep(1) 
        date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
        trimmedDate = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        logEntry = '{}\tINFO\t[{}]\t[Trade_Group]\t[17:demostroh]\t[default task-39]\t{}\n'.format(trimmedDate[:-3], sessionid, widgets[int(i)])
        logFile.write(logEntry)   
        logFile.write('=========================================================\n')
        #print(logEntry)
        #print('routine written in {}'.format(sessionid))
        global routineWritten 
        routineWritten = True

def generateSessionid():
    possibleChars = string.ascii_letters + string.digits
    return ''.join(random.choice(possibleChars) for i in range(16))



parser = argparse.ArgumentParser()
parser.add_argument("-f","--fixedRoutine",help="adds a fixed routine to the logfile")
parser.add_argument("-d","--days",help="set days to add to current day")
args = parser.parse_args()

daysDiff = 0
routineWritten = False
if args.days:
    daysDiff = int(args.days)
   #print("set days %s" % args.days)

date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
fileName = "multiversa-session.log." + date.strftime("%Y-%m-%d") +".log"

logfile = open(os.path.realpath('.') + '/multiversa-/' + fileName, "a+")
sessionid = generateSessionid()

k = random.randint(1,20)
#print(k)
for i in range(k): 
    sleep(1)
    date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
    trimmedDate = date.strftime("%Y-%m-%d %H:%M:%S.%f")
    arrayPos = random.randint(0,len(widgets)-1)
    logEntry = '{}\tINFO\t[{}]\t[Trade_Group]\t[17:demostroh]\t[default task-39]\t{}\n'.format(trimmedDate[:-3],sessionid,widgets[arrayPos])
    j = random.randint(0,10)
    if (j != 0 and i != 0 and i % j == 0 and  args.fixedRoutine and not routineWritten):
        #print(i)
        #print(routineWritten)
        fixedRoutine(logfile, sessionid)
        #print(routineWritten)
        #print(logEntry)
    #else:
        #print("hier komm ich auch hin")
    # vielleicht sollte ich hier die fixed routine hin machen und mit einer variable prüfen, ob es schonmal gemacht wurde. und dann nur bei jeden dritten mal (also mod 3) die variable wieder auf True setzen
    
    logfile.write(logEntry)
    logfile.write('=========================================================\n')
    #random.shuffle(widgets)

#fixedoutine(routine,f)

if (args.fixedRoutine and not routineWritten):
    #print("JAWOLL ALDER")
    args.fixedRoutine = args.fixedRoutine.split(',')
    fixedRoutine(logfile, sessionid)
    #print('at the end')
logfile.close()




