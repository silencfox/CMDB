import psycopg2
import os

# Configuración de conexión
DB_HOST = "wikidb"       # nombre del servicio Docker
DB_NAME = "wikijs"
DB_USER = "wikijs"
DB_PASS = "wikijsPass"

# Carpeta de salida
OUTPUT_DIR = "./documents"
os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    # Conexión a PostgreSQL
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    cursor = conn.cursor()

    # Consulta: ajusta la tabla si tu esquema es diferente
    cursor.execute("""
        SELECT id, title, content
        FROM pages
        WHERE content IS NOT NULL;
    """)

    rows = cursor.fetchall()

    for row in rows:
        page_id = row[0]
        title = row[1].replace(" ", "_")
        content = row[2]

        filename = f"{OUTPUT_DIR}/{title}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✅ Guardado: {filename}")

    cursor.close()
    conn.close()
    print("🎉 Exportación completa.")

except Exception as e:
    print(f"❌ Error: {e}")
