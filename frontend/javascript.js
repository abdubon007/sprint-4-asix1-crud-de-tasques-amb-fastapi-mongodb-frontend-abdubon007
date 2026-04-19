const API = "http://127.0.0.1:8000";
 
// CREATE - POST /books/
async function createBook() {
  const titol = document.getElementById("titol").value;
  const autor = document.getElementById("autor").value;
  const estat = document.getElementById("estat").value;
  const valoracio = parseInt(document.getElementById("valoracio").value);
  const categoria = document.getElementById("categoria").value;
  const persona = document.getElementById("persona").value;
 
  if (!titol || !autor || !persona) {
    document.getElementById("create-msg").innerText = "Error: títol, autor i persona són obligatoris.";
    return;
  }
 
  const res = await fetch(`${API}/books/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titol, autor, estat, valoracio, categoria, persona })
  });
 
  const data = await res.json();
  document.getElementById("create-msg").innerText = "Llibre creat! ID: " + data._id;
  loadBooks();
}
 
// READ ALL - GET /books/
async function loadBooks() {
  const res = await fetch(`${API}/books/`);
  const data = await res.json();
  const container = document.getElementById("book-list");
 
  if (data.books.length === 0) {
    container.innerHTML = "<p>No hi ha llibres.</p>";
    return;
  }
 
  container.innerHTML = data.books.map(b =>
    `<div>
      <b>${b.titol}</b> - ${b.autor} | Estat: ${b.estat} | Valoració: ${b.valoracio} | Categoria: ${b.categoria} | Persona: ${b.persona}
      <br><small>ID: ${b._id}</small>
    </div>`
  ).join("");
}
 
// READ ONE - GET /books/{id}
async function getBookById() {
  const id = document.getElementById("search-id").value;
  const res = await fetch(`${API}/books/${id}`);
 
  if (res.status === 404) {
    document.getElementById("book-detail").innerText = "Llibre no trobat.";
    return;
  }
 
  const b = await res.json();
  document.getElementById("book-detail").innerHTML =
    `<b>${b.titol}</b> - ${b.autor}<br>
     Estat: ${b.estat}<br>
     Valoració: ${b.valoracio}<br>
     Categoria: ${b.categoria}<br>
     Persona: ${b.persona}`;
}
 
// UPDATE - PUT /books/{id}
async function updateBook() {
  const id = document.getElementById("update-id").value;
  if (!id) {
    document.getElementById("update-msg").innerText = "Cal introduir un ID.";
    return;
  }
 
  const payload = {};
  const estat = document.getElementById("update-estat").value;
  const valoracio = document.getElementById("update-valoracio").value;
 
  if (estat) payload.estat = estat;
  if (valoracio) payload.valoracio = parseInt(valoracio);
 
  const res = await fetch(`${API}/books/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
 
  if (res.status === 404) {
    document.getElementById("update-msg").innerText = "Llibre no trobat.";
    return;
  }
 
  const data = await res.json();
  document.getElementById("update-msg").innerText = "Actualitzat! Estat: " + data.estat;
  loadBooks();
}
 
// DELETE - DELETE /books/{id}
async function deleteBook() {
  const id = document.getElementById("delete-id").value;
  const res = await fetch(`${API}/books/${id}`, { method: "DELETE" });
 
  if (res.status === 204) {
    document.getElementById("delete-msg").innerText = "Llibre eliminat correctament.";
    loadBooks();
  } else {
    document.getElementById("delete-msg").innerText = "Error: Llibre no trobat.";
  }
}
 
// Carregar llibres al iniciar la pàgina
window.onload = loadBooks;
