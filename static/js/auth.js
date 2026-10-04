localStorage.getItem("token") && document.body.dataset.page === "login" && localStorage.removeItem("token");
document.getElementById("form").addEventListener("submit", async e => {
  e.preventDefault();
  const f = Object.fromEntries(new FormData(e.target));
  const isSignup = document.body.dataset.page === "signup";
  try {
    const d = await api(isSignup ? "/signup" : "/login", { method: "POST", body: JSON.stringify(f) });
    if (isSignup) { toast(d.message); setTimeout(() => location.href = "/login", 900); }
    else { localStorage.setItem("token", d.token); localStorage.setItem("user", JSON.stringify(d.user)); location.href = "/home"; }
  } catch (x) { document.getElementById("msg").textContent = x.message; }
});
