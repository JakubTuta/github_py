from requests import get
from pprint import PrettyPrinter

BASE_URL = "https://free.currconv.com/"
API_KEY = "61ee0b3c39a1eea3eb06"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()['results']
    
    data = list(data.items())
    data.sort()
    
    return data


def print_currencies(currencies):
    for name, currency in currencies:
        name = currency['currencyName']
        _id = currency['id']
        symbol = currency.get("currencySymbol", "")
        print(f"{_id} - {name} - {symbol}")


def exchange_rate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = BASE_URL + endpoint
    data = get(url).json()
    
    if len(data) == 0:
        print("Invalid currency")
        return
    
    rate = list(data.values())[0]
    
    return rate


def convert(currency1, currency2, amount):
    rate = exchange_rate(currency1, currency2)
    if rate is None:
        return
    
    try:
        amount = float(amount)
    except:
        print("Invalid amount")
        return
    
    converted_amount = rate * amount
    return converted_amount


def main():
    print("KONWERTER WALUT\n")
    print("Lista dostępnych walut: lista")
    print("Kurs wymiany walut: kurs")
    print("Wymiana walut: wymianan")
    info = input("\nCo wybierasz: ")
    
    if info == "lista" or info == "Lista":
        data = get_currencies()
        print_currencies(data)
        
    elif info == "kurs" or info == "Kurs":
        curr1 = input("Podaj ID pierwszej waluty: ")
        curr2 = input("Podaj ID drugiej waluty: ")
        rate = exchange_rate(curr1, curr2)
        print(f"{curr1} -> {curr2} : {rate}")
        
    elif info == "wymiana" or info == "Wymiana":
        curr1 = input("Podaj ID pierwszej waluty: ")
        amount = input("Podaj ilość: ")
        curr2 = input("Podaj ID drugiej waluty: ")
        ilosc = convert(curr1, curr2, amount)
        print(f"{amount} {curr1} = {ilosc} {curr2}")
    
    else:
        print("Nieznana komenda")


if __name__ == "__main__":
    main()
