// -------------------------------------------------
// State
// -------------------------------------------------
let fractions = [];


// -------------------------------------------------
// Hjælpefunktioner
// -------------------------------------------------
function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function generateRandomFractions(count = 12) {
    const result = [];
    const maxDenominator = 12;

    while (result.length < count) {
        const d = randomInt(2, maxDenominator);
        const n = randomInt(1, d - 1);

        if (!result.some(f => f.n === n && f.d === d)) {
            result.push({ n, d });
        }
    }

    return result;
}

function renderFractions() {
    const grid = document.getElementById("fraction-grid");
    grid.innerHTML = "";

    fractions.forEach((f, index) => {
        const div = document.createElement("div");
        div.className = "fraction-preview";
        div.textContent = `${f.n}/${f.d}`;

        div.addEventListener("click", () => editFraction(index));

        grid.appendChild(div);
    });
}


// -------------------------------------------------
// Redigér brøk
// -------------------------------------------------
function editFraction(index) {
    const modal = document.getElementById("edit-modal");
    const inputs = modal.querySelectorAll("input");
    const cancelBtn = modal.querySelector(".secondary-button");
    const saveBtn = modal.querySelector(".primary-button");

    inputs[0].value = fractions[index].n;
    inputs[1].value = fractions[index].d;

    modal.classList.remove("hidden");

    cancelBtn.onclick = () => {
        modal.classList.add("hidden");
    };

    saveBtn.onclick = () => {
        const n = parseInt(inputs[0].value, 10);
        const d = parseInt(inputs[1].value, 10);

        if (!Number.isInteger(n) || !Number.isInteger(d) || n <= 0 || d <= n) {
            alert("Ugyldig brøk");
            return;
        }

        fractions[index] = { n, d };
        modal.classList.add("hidden");
        renderFractions();
    };
}


// -------------------------------------------------
// Læs repræsentationer (robust)
// -------------------------------------------------
function getSelectedRepresentations() {
    const checkboxes = document.querySelectorAll(
        'input[type="checkbox"]:checked'
    );

    const values = Array.from(checkboxes).map(cb => cb.value);

    // Hvis ingen er valgt, lad backend styre defaults
    if (values.length === 0) {
        return null;
    }

    return values;
}


// -------------------------------------------------
// Events
// -------------------------------------------------
document.getElementById("generate-random").addEventListener("click", () => {
    fractions = generateRandomFractions();
    renderFractions();
});

document.getElementById("regenerate").addEventListener("click", () => {
    fractions = generateRandomFractions();
    renderFractions();
});

document.getElementById("generate-pdf").addEventListener("click", async () => {
    if (fractions.length === 0) {
        alert("Der er ingen brøker at generere PDF for.");
        return;
    }

    const representations = getSelectedRepresentations();

    const response = await fetch("/generate-pdf", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            fractions: fractions,
            representations: representations
        })
    });

    if (!response.ok) {
        alert("Der opstod en fejl ved generering af PDF.");
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
});
