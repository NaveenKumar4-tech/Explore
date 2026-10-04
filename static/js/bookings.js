requireAuth(); renderNav();
const list = document.getElementById("list"), dlg = document.getElementById("dlg"), ef = document.getElementById("edit");
let bookings = [], editing = null;
async function load() { bookings = await api("/bookings"); draw(); }
function draw() {
  list.innerHTML = bookings.map(b => `
    <div class="trip ${b.status}">
      <img src="${b.country.image}" alt="">
      <div class="info"><h3>${b.country.name} <span class="badge ${b.status}">${b.status}</span></h3>
        <p>📅 ${b.travel_date} &nbsp; 👥 ${b.travelers} traveler(s) &nbsp; 💰 ${money(b.total_price)}</p></div>
      <div class="actions">${b.status === "confirmed" ? `
        <button class="btn small" onclick="openEdit(${b.id})">Edit</button>
        <button class="btn small danger" onclick="cancelTrip(${b.id})">Cancel</button>` : ""}</div>
    </div>`).join("") || `<p>No trips yet. <a href="/home">Explore destinations</a></p>`;
}
function openEdit(id) {
  editing = bookings.find(b => b.id === id);
  ef.travel_date.value = editing.travel_date; ef.travelers.value = editing.travelers;
  ef.travel_date.min = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
  document.getElementById("emsg").textContent = ""; dlg.showModal();
}
ef.addEventListener("submit", async e => {
  e.preventDefault();
  try {
    await api("/bookings/" + editing.id, { method: "PUT", body: JSON.stringify({ travel_date: ef.travel_date.value, travelers: ef.travelers.value }) });
    dlg.close(); toast("Booking updated"); load();
  } catch (x) { document.getElementById("emsg").textContent = x.message; }
});
async function cancelTrip(id) {
  if (!confirm("Cancel this trip?")) return;
  try { await api("/bookings/" + id, { method: "DELETE" }); toast("Trip cancelled"); load(); }
  catch (x) { toast(x.message, true); }
}
load();


// =============== Responsive
let sidebtn=document.querySelector(".menu")
let navlinks = document.querySelector(".nav-links")
sidebtn.addEventListener("click",()=>{
    navlinks.classList.toggle("side")
})

document.addEventListener("pointerdown",(e)=>{
    if(!sidebtn.contains(e.target) && !navlinks.contains(e.target)){
        console.log("working")
        navlinks.classList.remove("side")
    }
})