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


def fixedRoutine(logFile, sessionID):
    args.fixedRoutine = args.fixedRoutine.split(',')
    for widget in args.fixedRoutine:
        #sleep(1)
        date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
        trimmedDate = date.strftime("%Y-%m-%d %H:%M:%S.%f")
        logEntry = f"{trimmedDate[:-3]}\tINFO\t[{sessionID}]\t[Trade_Group]\t[17:demostroh]\t" \
                   f"[default task-39]\t{widgets[int(widget)]}\n"
        logFile.write(logEntry)
        logFile.write('=========================================================\n')
        global routineWritten
        routineWritten = True


def generateSessionID():
    possibleChars = string.ascii_letters + string.digits
    return ''.join(random.choice(possibleChars) for i in range(16))

# This function determines whether the fixed routine should be written. It checks if the randomValue is a multiple
# of the current widgetCnt and if the command line parameter for fixed routine is set. Also it checks if a routine
# was written before.
def shouldWriteRoutine(randomValue, widgetCnt):
    return randomValue != 0 and widgetCnt != 0 and widgetCnt % randomValue == 0 \
           and args.fixedRoutine and not routineWritten


parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fixedRoutine", help="adds a fixed routine to the logfile")
parser.add_argument("-d", "--days", help="set days to add to current day")
args = parser.parse_args()

daysDiff = 0
routineWritten = False
if args.days:
    daysDiff = int(args.days)


def main():
    date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
    fileName = "multiversa-session.log." + date.strftime("%Y-%m-%d") + ".log"
    sessionID = generateSessionID()
    numberOfWidgetsInSession = random.randint(1, 20)

    try:
        open(os.path.realpath('.') + '/multiversa-/' + fileName, "a+")
    except FileNotFoundError:
        os.mkdir(os.path.realpath('.') + "/multiversa-/")

    # After a check if the directory exists where the logfiles should be stored write the randomly chosen data in the
    # logfile
    with open(os.path.realpath('.') + '/multiversa-/' + fileName, "a+") as logfile:
        for widgetCnt in range(numberOfWidgetsInSession):
            #sleep(1)
            date = datetime.datetime.now() + datetime.timedelta(days=daysDiff)
            trimmedDate = date.strftime("%Y-%m-%d %H:%M:%S.%f")
            arrayPos = random.randint(0, len(widgets)-1)
            logEntry = f"{trimmedDate[:-3]}\tINFO\t[{sessionID}]\t[Trade_Group]\t[17:demostroh]\t" \
                       f"[default task-39]\t{widgets[arrayPos]}\n"

            # If the session should contain a fixed routine write it at an random position in the file
            randomValue = random.randint(0, 10)
            if shouldWriteRoutine(randomValue, widgetCnt):
                fixedRoutine(logfile, sessionID)

            logfile.write(logEntry)
            logfile.write('=========================================================\n')

        # Write the fixed routine at the end of the file if it was not written before
        if args.fixedRoutine and not routineWritten:
            fixedRoutine(logfile, sessionID)


if __name__ == "__main__":
    main()

