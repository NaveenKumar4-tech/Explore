/* My trips: list, edit, cancel */
(async function () {
  if (!requireAuth()) return;
  const list = document.getElementById("trip-list");
  const modal = document.getElementById("edit-modal");
  const form = document.getElementById("edit-form");
  const errEl = document.getElementById("edit-error");
  const totalEl = document.getElementById("edit-total");
  let bookings = [], filter = "all", editing = null;

  function render() {
    const rows = bookings.filter((b) => filter === "all" || b.status === filter);
    if (!rows.length) {
      list.innerHTML = `<div class="empty"><h3>${filter === "all" ? "No trips yet" : "Nothing here"}</h3>
        <p class="muted">${filter === "all" ? "Choose a country and book your first trip." : "No trips with this status."}</p>
        ${filter === "all" ? '<a class="btn btn-primary" href="/home">Browse countries</a>' : ""}</div>`;
      return;
    }
    list.innerHTML = rows.map((b) => `
      <article class="pass ${b.status}">
        <div class="pass-img"><img src="${esc(b.country.image)}" alt="${esc(b.country.name)}"></div>
        <div class="pass-body">
          <h3>${esc(b.place.name)}</h3>
          <div class="ref">${esc(b.country.name)} - Ref ${esc(b.reference)}</div>
          <div class="rows">
            <div><span>Travel date</span><b>${prettyDate(b.travel_date)}</b></div>
            <div><span>Travelers</span><b>${b.travelers}</b></div>
            <div><span>Duration</span><b>${b.place.duration_days} days</b></div>
          </div>
          ${b.notes ? `<p class="note">Note: ${esc(b.notes)}</p>` : ""}
        </div>
        <div class="pass-side">
          <span class="status ${b.status}">${b.status === "confirmed" ? "Confirmed" : "Cancelled"}</span>
          <span class="total">${money(b.total_price)}</span>
          ${b.status === "confirmed" ? `<div class="pass-actions">
            <button class="btn btn-ghost" data-edit="${b.id}" type="button">Edit</button>
            <button class="btn btn-danger" data-cancel="${b.id}" type="button">Cancel</button></div>` : ""}
        </div>
      </article>`).join("");
  }

  async function load() {
    try { ({ bookings } = await api("/api/bookings")); render(); }
    catch (err) { list.innerHTML = `<p class="form-error">${esc(err.message)}</p>`; }
  }

  document.querySelectorAll(".tab").forEach((t) => t.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((x) => x.classList.remove("active"));
    t.classList.add("active"); filter = t.dataset.filter; render();
  }));

  const updateTotal = () => {
    const n = Math.max(1, parseInt(form.travelers.value, 10) || 1);
    totalEl.textContent = editing ? money(editing.place.price_per_person * n) : "$0";
  };
  form.travelers.addEventListener("input", updateTotal);

  const closeModal = () => { modal.hidden = true; };
  modal.addEventListener("click", (e) => { if (e.target === modal || e.target.hasAttribute("data-close")) closeModal(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeModal(); });

  list.addEventListener("click", async (e) => {
    const editId = e.target.dataset.edit, cancelId = e.target.dataset.cancel;
    if (editId) {
      editing = bookings.find((b) => b.id === Number(editId));
      document.getElementById("edit-sub").textContent = `${editing.place.name}, ${editing.country.name} (${editing.reference})`;
      form.travel_date.min = tomorrowISO();
      form.travel_date.value = editing.travel_date;
      form.travelers.value = editing.travelers;
      form.notes.value = editing.notes;
      errEl.textContent = "";
      updateTotal();
      modal.hidden = false;
    }
    if (cancelId) {
      const b = bookings.find((x) => x.id === Number(cancelId));
      if (!confirm(`Cancel your trip to ${b.country.name} (${b.place.name})?`)) return;
      try { await api(`/api/bookings/${b.id}/cancel`, { method: "POST" }); toast("Trip cancelled."); load(); }
      catch (err) { toast(err.message, "error"); }
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    errEl.textContent = "";
    try {
      await api(`/api/bookings/${editing.id}`, { method: "PUT", body: {
        travel_date: form.travel_date.value, travelers: form.travelers.value, notes: form.notes.value } });
      closeModal(); toast("Trip updated."); load();
    } catch (err) { errEl.textContent = err.message; }
  });

  load();
})();
