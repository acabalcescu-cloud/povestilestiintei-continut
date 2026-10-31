# Tema copil (atleticos-child)

- `atleticos-child.zip` – ultima versiune a temei copil; `versiune.txt` – numărul ei; `sha256.txt` – amprenta arhivei.
- Site-ul o instalează la `POST /wp-json/ps/v1/tema` (doar administratori), care descarcă arhiva de aici,
  verifică amprenta SHA-256 și suprascrie tema copil. Funcționează începând cu versiunea 1.18.1, instalată o dată manual.
