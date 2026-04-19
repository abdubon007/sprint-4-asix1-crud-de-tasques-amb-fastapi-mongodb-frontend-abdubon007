# Documentació Sprint 4 — Gestor de Llibres
 
**Alumne:** Abdullah Muhammad Jabeen  
**Curs:** ASIX1 — 25/26  
**Professors:** Maria Merino / Eros Vilar
 
---
 
## Introducció
 
En aquest sprint he desenvolupat una aplicació web completa per gestionar una llista de llibres. L'aplicació té un backend amb FastAPI connectat a MongoDB Atlas, i un frontend fet amb HTML, CSS i JavaScript que permet fer totes les operacions CRUD des del navegador.
 
- URL de l'API: `http://127.0.0.1:8000`
- Col·lecció MongoDB: `books`
---
 
## 1. Documentació automàtica — Swagger
 
FastAPI genera automàticament una interfície Swagger accessible a `http://127.0.0.1:8000/docs`. Des d'aquí es poden veure i provar tots els endpoints de l'API.
 <img width="710" height="817" alt="Captura de pantalla 2026-04-19 234334" src="https://github.com/user-attachments/assets/be3a2e2e-597c-4d15-b04c-386d72e8f460" />

 
---
 
## 2. Tests amb Postman
 
He creat una col·lecció a Postman amb totes les peticions CRUD per comprovar que l'API funciona correctament.
 
### 2.1 POST /books/ — Crear un llibre
 
He enviat un JSON amb les dades del llibre. La resposta ha estat **201 Created** amb l'`_id` generat per MongoDB.
 
```json
{
  "titol": "Harry Potter i la Pedra Filosofal",
  "autor": "J.K. Rowling",
  "estat": "pendent",
  "valoracio": 5,
  "categoria": "fantasia",
  "persona": "Abdullah"
}
```
 <img width="710" height="817" alt="Captura de pantalla 2026-04-19 234334" src="https://github.com/user-attachments/assets/ba28b960-90ff-41c7-af73-931243f6726a" />

 
---
 
### 2.2 GET /books/ — Llistar tots els llibres
 
He comprovat que el llibre creat apareix a la llista. No cal enviar cap body. La resposta ha estat **200 OK**.
<img width="953" height="965" alt="Captura de pantalla 2026-04-19 234201" src="https://github.com/user-attachments/assets/45e1b813-ba56-4777-8ad2-fcfe34a44ab1" /> 

 
---
 
### 2.3 GET /books/{id} — Obtenir un llibre per ID
 
He utilitzat l'`_id` retornat en el POST per obtenir el llibre concret. La resposta ha estat **200 OK**.
 
<img width="950" height="832" alt="Captura de pantalla 2026-04-19 234509" src="https://github.com/user-attachments/assets/a72fe6ad-9f55-4dcb-bfa6-33039d7f1a54" />
 
---
 
### 2.4 PUT /books/{id} — Actualitzar un llibre
 
He canviat l'estat a `llegit` i la valoració. Només he enviat els camps que volia modificar. La resposta ha estat **200 OK**.
 
```json
{
  "estat": "llegit",
  "valoracio": 4
}
```
 
<img width="705" height="812" alt="image" src="https://github.com/user-attachments/assets/9509c4a8-4603-4445-b8d0-472de5b2454c" />

 
---
 
### 2.5 DELETE /books/{id} — Eliminar un llibre
 
He eliminat el llibre pel seu ID. La resposta **204 No Content** confirma que s'ha eliminat correctament.
 
<img width="950" height="1032" alt="Captura de pantalla 2026-04-19 234609" src="https://github.com/user-attachments/assets/62346938-710e-4131-86bb-c94b0f20c8cc" />

 
---
 
## 3. Frontend
 
He creat una interfície web senzilla amb HTML, CSS i JavaScript que permet fer totes les operacions CRUD des del navegador.
 
### Llistar tots els llibres
 
<img width="907" height="253" alt="Captura de pantalla 2026-04-20 001912" src="https://github.com/user-attachments/assets/495b0a97-d8ec-4d9b-91a0-7e60a1513901" />

 
### Buscar per ID
 

<img width="836" height="270" alt="Captura de pantalla 2026-04-20 001926" src="https://github.com/user-attachments/assets/d8235c67-d92c-458b-bd50-8085760ff534" />

 
### Actualitzar un llibre
 
<img width="821" height="571" alt="Captura de pantalla 2026-04-20 001945" src="https://github.com/user-attachments/assets/4c8debda-107c-4065-9fe3-e4ab048d8dd9" />
 
### Eliminar un llibre
 
<img width="621" height="141" alt="Captura de pantalla 2026-04-20 002002" src="https://github.com/user-attachments/assets/781b3c07-bc1d-4ed5-8129-7fe28160800a" />

 
---
 
## 4. Conclusions
 
Tots els endpoints han funcionat correctament:
 
| Endpoint | Codi | Resultat |
|----------|------|----------|
| POST /books/ | 201 | Llibre creat correctament |
| GET /books/ | 200 | Llistat complet retornat |
| GET /books/{id} | 200 | Llibre concret trobat |
| PUT /books/{id} | 200 | Llibre actualitzat correctament |
| DELETE /books/{id} | 204 | Llibre eliminat (No Content) |<img width="710" height="817" alt="Captura de pantalla 2026-04-19 234334" src="https://github.com/user-attachments/assets/c5384ac4-9ac3-4e4a-8467-a1b2e244616f" />
