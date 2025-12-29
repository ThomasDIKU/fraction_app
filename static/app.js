console.log("app.js loaded");

// ---------- State ----------
let fractions = [];
let selectedIndex = null;

// ---------- Config ----------
const FRACTION_COUNT = 12;
const MAX_DENOMINATOR = 10;

// ---------- DOM ----------
const grid = document.getElementById("fraction-grid");
const generateBtn = document.getElementById("generate-random");
const regenerateBtn = document.getElementById("regenerate");
const pdfBtn = document.getElementById("generate-pdf");

const modal = document.getElementById("edit-modal");
const saveBtn = modal.querySelector(".primary-button");
const cancelBtn = modal.querySelector(".secondary-button");
const numeratorInput = modal.querySelector("input[min='1']");
const denominatorInput = modal.querySelector("input[min='2']");

// ---------- Helpers ----------
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// ---------- Generate ----------
function generateRandomFractions() {
    console.log("Generating random fractions");
    fractions = [];

    for (let i = 0; i < FRACTION_COUNT; i++) {
        const d = randomInt(2, MAX_DENOMINATOR);
        const n = randomInt(1, d - 1);
        fractions.push({ n, d });
    }

    render();
}

// ---------- Render ----------
function render() {
    console.log("Rendering fractions", fractions);
    grid.innerHTML = "";

    fractions.forEach((frac, index) => {
        const card = document.createElement("div");
        card.className = "fraction-card";

        card.innerHTML = `
            <span class="numerator">${frac.n}</span>
            <span class="divider"></span>
            <span class="denominator">${frac.d}</span>
        `;

        card.addEventListener("click", () => openModal(index));
        grid.appendChild(card);
    });
}

// ---------- Modal ----------
function openModal(index) {
    selectedIndex = index;
    numeratorInput.value = fractions[index].n;
    denominatorInput.value = fractions[index].d;
    modal.classList.remove("hidden");
}

function closeModal() {
    modal.classList.add("hidden");
    selectedIndex = null;
}

saveBtn.addEventListener("click", () => {
    const n = parseInt(numeratorInput.value);
    const d = parseInt(denominatorInput.value);

    if (!(n > 0 && d > 0 && n < d)) {
        alert("Ugyldig brøk. Tæller skal være mindre end nævner.");
        return;
    }

    fractions[selectedIndex] = { n, d };
    closeModal();
    render();
});

cancelBtn.addEventListener("click", closeModal);

// ---------- PDF ----------
pdfBtn.addEventListener("click", async () => {
    console.log("Generate PDF clicked");

    try {
        const response = await fetch("/generate-pdf", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ fractions })
        });

        console.log("Response status:", response.status);

        if (!response.ok) {
            alert("Serverfejl ved generering af PDF");
            return;
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = "broekkort.pdf";
        document.body.appendChild(a);
        a.click();

        a.remove();
        window.URL.revokeObjectURL(url);

    } catch (err) {
        console.error("Fetch error:", err);
        alert("Kunne ikke kontakte serveren");
    }
});

// ---------- Events ----------
generateBtn.addEventListener("click", generateRandomFractions);
regenerateBtn.addEventListener("click", generateRandomFractions);

// ---------- Init ----------
generateRandomFractions();
