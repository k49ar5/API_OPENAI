import os
import requests


API_URL = "https://api.openai.com/v1/chat/completions"
API_KEY = "Wstaw_tutaj_swoj_klucz_API"  #TODO zamienić klucz API


def wczytaj_plik(sciezka):
    if not os.path.exists(sciezka):
        raise FileNotFoundError(f"Plik {sciezka} nie istnieje.")
    with open(sciezka, 'r', encoding='utf-8') as plik:
        return plik.read()


def wyslij_do_openai(tresc, prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are an assistant that generates clean and structured HTML content."},
            {"role": "user", "content": f"{prompt}\n\n{tresc}"}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Błąd API: {response.status_code} - {response.text}")
    return response.json()["choices"][0]["message"]["content"]


def zapisz_plik(sciezka, tresc):
    with open(sciezka, 'w', encoding='utf-8') as plik:
        plik.write(tresc)


def main():

    sciezka_wejsciowa = "artykul.txt"
    sciezka_wyjsciowa = "artykul.html"


    tresc_artykulu = wczytaj_plik(sciezka_wejsciowa)

    prompt = (
        "Generate HTML code for the following article. Use appropriate tags like <h1>, <h2>, <p>, "
        "<img> with placeholders (src='image_placeholder.jpg') and descriptive alt attributes. "
        "Do not include <html> or <head> tags. Add <figcaption> for image captions."
    )


    wygenerowany_html = wyslij_do_openai(tresc_artykulu, prompt)


    zapisz_plik(sciezka_wyjsciowa, wygenerowany_html)
    print(f"Wygenerowany plik HTML zapisano jako {sciezka_wyjsciowa}")


if __name__ == "__main__":
    main()
