const API = "/api";
const getToken = () => localStorage.getItem("token");

async function api(path, opts = {}) {
  const headers = { "Content-Type": "application/json" };
  if (getToken()) headers.Authorization = "Bearer " + getToken();
  const res = await fetch(API + path, { ...opts, headers });
  const data = await res.json().catch(() => ({}));
  if ((res.status === 401 || res.status === 422) && getToken() && !path.startsWith("/login")) logout();
  if (!res.ok) throw new Error(data.error || data.msg || "Something went wrong");
  return data;
}
function requireAuth() { if (!getToken()) location.href = "/login"; }
function logout() { localStorage.clear(); location.href = "/login"; }
const money = n => "$" + Number(n).toLocaleString();
function toast(msg, bad) {
  const t = document.createElement("div");
  t.className = "toast" + (bad ? " bad" : "");
  t.textContent = msg; document.body.appendChild(t);
  setTimeout(() => t.remove(), 3000);
}
function renderNav() {
  const u = JSON.parse(localStorage.getItem("user") || "{}");
  document.getElementById("nav").innerHTML = `
    <a class="brand" href="/home"><img src="/static/images/logo.png"></a>
    <div><ul class="nav-links" id="navLinks">
            <li><a href="#home">Home</a></li>
            <li><a href="#grid" data-nav="home">Countries</a></li>
           <li> <a href="/bookings" data-nav="trips">My trips</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    <span class="hi">Hi, ${u.name || "Traveler"}</span><button class="btn small ghost" onclick="logout()">Logout</button> <img class="menu" src="/static/images/menu.svg" /> </div>`;
}
