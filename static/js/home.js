requireAuth(); renderNav();
let all = [];
const grid = document.getElementById("grid");
function draw(list) {
  grid.innerHTML = list.map(c => `

    <a class="card" href="/country/${c.slug}">
      <img src="${c.image}" alt="${c.name}" loading="lazy">
      <div class="card-body"><h3>${c.name}</h3><p>${c.tagline}</p>
      <span class="price">from ${money(c.price)} / person</span></div></a>`).join("") || "<p>No destinations found.</p>";
}
api("/countries").then(d => { all = d; draw(d); });

let searchInput = document.getElementById("search")
document.querySelector(".search-btn").addEventListener("click", e =>{
    const value =searchInput.value.toLowerCase();
    const result = all.filter(c => c.name.toLowerCase().includes(value));
    draw(result)

    grid.scrollIntoView({
        "block":"center",
        "behavior":"smooth"
    })
})



// ==============================
// COUNTER ANIMATION
// ==============================

const counters =
    document.querySelectorAll(".counter");

let counterStarted = false;

function startCounters() {

    if (counterStarted) return;

    counterStarted = true;

    counters.forEach(counter => {

        const target =
            Number(counter.dataset.target);

        let current = 0;

        const increment =
            Math.ceil(target / 80);

        const updateCounter = () => {

            current += increment;

            if (current >= target) {

                counter.textContent =
                    target.toLocaleString();

                return;

            }

            counter.textContent =
                current.toLocaleString();

            requestAnimationFrame(updateCounter);

        };

        updateCounter();

    });

}


// Start counter when stats are visible

const statsSection =
    document.querySelector(".stats");

const observer =
    new IntersectionObserver(
        entries => {

            entries.forEach(entry => {

                if (entry.isIntersecting) {

                    startCounters();

                }

            });

        },
        {
            threshold: 0.3
        }
    );

observer.observe(statsSection);

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