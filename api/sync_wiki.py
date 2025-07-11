import requests
import os

API_URL = "http://wiki:3000/graphql"  # Usa el nombre del servicio Docker o URL real si accedes externamente

# 🔧 Reemplaza con tu token generado en Wiki.js
HEADERS = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcGkiOjEsImdycCI6MSwiaWF0IjoxNzUyMTA0ODg5LCJleHAiOjE3ODM2NjI0ODksImF1ZCI6InVybjp3aWtpLmpzIiwiaXNzIjoidXJuOndpa2kuanMifQ.CQ3sUxW7L1Dj6_ogoL_7N7NLwU4oozPlOSODH9VJdudCc17oCjz7cI5j9jqhf2iaValr40RMGwkrKQ6rYznFHm0OIaZOTiwdTYMLyIJ-TjR9Nm0e6HjOuHS6mg3t1E1k766xScbdP64-Mm2kS0qY43hOxDbB-QcYax2EmDKfBmD4VYGe4Zuru7QsdXLeM93yGHTpaZcjDZVLRipYGx5_IQ_p1Z3o9NacWGbAUCikDpREfYg9N92aHlPL5iddGrMPuVPbs1-f8RxBTvlr98Begz9zE5KwFIamxNxDaV-Fg4EVrtRKt4JRvFDo0lGMEr51htZvwQL--d3zVgzqTu70rQ"}

def download_wiki_pages():
    query = """
    {
      pages {
        list (orderBy: TITLE) {
          id
          path
          title
        }
      }
    }
    """

    response = requests.post(API_URL, json={"query": query}, headers=HEADERS)
    data = response.json()

    os.makedirs("./documents", exist_ok=True)

    for page in data["data"]["pages"]["list"]:
        filename = f"./documents/{page['title'].replace(' ', '_')}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(page["content"])
        print(f"✅ Guardado: {filename}")

if __name__ == "__main__":
    download_wiki_pages()
