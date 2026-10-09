// CAPA DE PRESENTACIÓN (UI): dibuja la pantalla y hace peticiones HTTP a la API.
const COUNT = Number(document.body.dataset.count);
const MAX = Number(document.body.dataset.max);
const selected = new Set();

const $ = (id) => document.getElementById(id);
const grid = $("grid");

for (let n = 1; n <= MAX; n++) {
  const b = document.createElement("button");
  b.className = "num";
  b.textContent = n;
  b.dataset.n = n;
  b.onclick = () => toggle(n);
  grid.appendChild(b);
}

function toggle(n) {
  if (selected.has(n)) selected.delete(n);
  else if (selected.size < COUNT) selected.add(n);
  render();
}

function render() {
  grid.querySelectorAll(".num").forEach((b) =>
    b.classList.toggle("on", selected.has(Number(b.dataset.n)))
  );
  const list = [...selected].sort((a, b) => a - b);
  $("selected").textContent = "Elegidos: " + (list.length ? list.join(", ") : "–");
}

function balls(nums, hits = []) {
  return nums
    .map((n) => `<span class="ball ${hits.includes(n) ? "hit" : ""}">${n}</span>`)
    .join("");
}

function showTrace(steps) {
  $("trace-card").classList.remove("hidden");
  $("trace").innerHTML = steps
    .map((s) => {
      const cls = s.layer.startsWith("Lógica") ? "logic" : "api";
      return `<li><span class="layer ${cls}">${s.layer}</span>${s.action}<span class="ms">${s.ms} ms</span></li>`;
    })
    .join("");
}

$("btn-clear").onclick = () => {
  selected.clear();
  $("error").textContent = "";
  render();
};

$("btn-quick").onclick = async () => {
  const res = await fetch("/api/quickpick");
  const data = await res.json();
  selected.clear();
  data.ticket.forEach((n) => selected.add(n));
  $("error").textContent = "";
  render();
  showTrace(data.trace);
};

$("btn-play").onclick = async () => {
  const ticket = [...selected].sort((a, b) => a - b);
  const res = await fetch("/api/jugar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ticket }),
  });
  const data = await res.json();
  showTrace(data.trace);

  if (!res.ok) {
    $("error").textContent = data.error;
    $("result").classList.add("hidden");
    return;
  }
  $("error").textContent = "";
  $("result").classList.remove("hidden");
  const title = $("result-title");
  title.textContent = data.won
    ? `🎉 ${data.prize} (${data.match_count} aciertos)`
    : `Sin premio (${data.match_count} aciertos)`;
  title.className = data.won ? "win" : "lose";
  $("winning").innerHTML = balls(data.winning, data.matches);
  $("ticket").innerHTML = balls(data.ticket, data.matches);
};

render();
