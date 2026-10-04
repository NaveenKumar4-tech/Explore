requireAuth(); renderNav();
const slug = location.pathname.split("/").pop();
const box = document.getElementById("detail");
api("/countries/" + slug).then(c => {
  document.title = c.name + " – Explore";
  box.innerHTML = `
    <div class="banner" style="background-image:linear-gradient(transparent,rgba(0,0,0,.65)),url('${c.image}')">
      <h1>${c.name}</h1><p>${c.tagline}</p></div>
    <div class="cols">
      <div><h2>About</h2><p>${c.description}</p>
        <h2>Highlights</h2><ul class="hl">${c.highlights.map(h => `<li>${h}</li>`).join("")}</ul>
        <div class="facts"><div><b>Best time</b>${c.best_time}</div><div><b>Currency</b>${c.currency}</div><div><b>Language</b>${c.language}</div></div></div>
      <form class="panel" id="book">
        <h2>Book this trip</h2><p class="price">${money(c.price)} <small>/ person</small></p>
        <label>Travel date<input type="date" name="travel_date" required></label>
        <label>Travelers<input type="number" name="travelers" min="1" max="20" value="1" required></label>
        <p class="total">Total: <b id="total">${money(c.price)}</b></p>
        <button class="btn">Confirm booking</button><p class="error" id="msg"></p></form>
    </div>`;
  const f = document.getElementById("book");
  const tomorrow = new Date(Date.now() + 864e5).toISOString().slice(0, 10);
  f.travel_date.min = tomorrow; f.travel_date.value = tomorrow;
  f.travelers.addEventListener("input", () => document.getElementById("total").textContent = money(c.price * (f.travelers.value || 0)));
  f.addEventListener("submit", async e => {
    e.preventDefault();
    try {
      await api("/bookings", { method: "POST", body: JSON.stringify({ country_id: c.id, travel_date: f.travel_date.value, travelers: f.travelers.value }) });
      toast("Trip booked! 🎉"); setTimeout(() => location.href = "/bookings", 800);
    } catch (x) { document.getElementById("msg").textContent = x.message; }
  });
}).catch(() => box.innerHTML = "<p>Country not found. <a href='/home'>Back</a></p>");


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