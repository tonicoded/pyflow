

function toggleDarkMode() {
    let body = document.body;
    let logo = document.getElementById("logo");

    if (!logo) {
        console.error("⚠️ ERROR: Logo element niet gevonden in toggleDarkMode()");
        return;
    }

    body.classList.toggle("light-mode");

    let isLightMode = body.classList.contains("light-mode");

    localStorage.setItem("theme", isLightMode ? "light" : "dark");

    // 🚀 Forceer herladen van het logo met een unieke URL om caching te omzeilen
    let timestamp = new Date().getTime();
    logo.src = isLightMode ? `/static/logo-light.png?t=${timestamp}` : `/static/logo.png?t=${timestamp}`;

    console.log(`🔄 Thema gewijzigd naar ${isLightMode ? "light" : "dark"} mode, logo aangepast naar: ${logo.src}`);
}


function toggleMenu() {
    let menu = document.getElementById("menu-content");
    let menuIcon = document.getElementById("menu-icon");

    menu.classList.toggle("active");

    if (menu.classList.contains("active")) {
        menuIcon.innerHTML = "✖"; // Icoon veranderen naar kruisje
    } else {
        menuIcon.innerHTML = "☰"; // Terug naar hamburger
    }
}




let subtitleInterval;
const subtitles = [
    "Efficiënte automatiseringsoplossingen voor bedrijven",
    "Bespaar tijd met slimme scripts",
    "Maatwerk software voor elk bedrijf",
    "Jouw workflow, geautomatiseerd",
    "Laat technologie voor je werken"
];

let index = 0;
let subtitle = document.getElementById("subtitle");
let title = document.getElementById("glitch-text");

// ✅ Typewriter functie
function typeWriterEffect(text, element, speed = 50, callback = null) {
    element.textContent = ""; // Gebruik textContent om sneller te updaten zonder layout shift
    let i = 0;

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed);
        } else if (callback) {
            setTimeout(callback, 2000); // Wacht 2 sec voordat de volgende tekst start
        }
    }
    type();
}

// ✅ Wisselt automatisch de ondertitels (met tab-check)
function cycleSubtitles() {
    if (document.hidden) return; // 🔹 Stop updates als tabblad niet actief is

    subtitle.style.opacity = "0"; // Fade-out effect
    setTimeout(() => {
        index = (index + 1) % subtitles.length; // Volgende zin
        typeWriterEffect(subtitles[index], subtitle, 50, () => {
            subtitle.style.opacity = "1"; // Fade-in effect
        });
    }, 500); // Wacht 500ms voordat de nieuwe tekst wordt getypt
}



// ✅ Start ondertitel wisselen als tabblad actief wordt
function startSubtitleRotation() {
    if (subtitleInterval) clearInterval(subtitleInterval); // Verwijder oude interval
    subtitleInterval = setInterval(cycleSubtitles, 5000); // ✅ Wissel elke 5 sec
}

// ✅ Zet de H1-titel en toon direct de eerste ondertitel
title.innerHTML = ""; // Leegmaken voor effect
subtitle.innerHTML = ""; // Leegmaken voor effect

typeWriterEffect("PyTimize", title, 100, function () {
    // ✅ Direct de eerste ondertitel zonder vertraging tonen
    typeWriterEffect(subtitles[index], subtitle, 50, () => {
        subtitle.style.opacity = "1"; // Fade-in effect
        startSubtitleRotation(); // ✅ Start wisselcyclus
    });
});

// ✅ Stop en herstart de wisselcyclus als de gebruiker terugkeert naar het tabblad
document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
        startSubtitleRotation(); // 🔹 Herstart interval als gebruiker terugkeert
    }
});

document.addEventListener("DOMContentLoaded", function () {
    
    const canvas = document.getElementById("backgroundCanvas");
    const ctx = canvas ? canvas.getContext("2d") : null;
    const logo = document.getElementById("logo");

    if (!logo) {
        console.error("⚠️ ERROR: Logo element niet gevonden! Controleer of <img id='logo'> in index.html staat.");
        return;
    }

    function resizeCanvas() {
        if (canvas) {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
    }

    resizeCanvas();
    window.addEventListener("resize", resizeCanvas);

    // ✅ Correcte paden naar de logo’s
    const darkLogo = "/static/logo.png";
    const lightLogo = "/static/logo-light.png";

    // ✅ Thema ophalen en toepassen
    let savedTheme = localStorage.getItem("theme");

    if (!savedTheme) {
        console.warn("⚠️ Geen thema gevonden in localStorage, standaard dark mode ingesteld.");
        localStorage.setItem("theme", "dark"); // Standaard dark mode
        savedTheme = "dark";
    }

    console.log("🎨 Thema opgeslagen in localStorage:", savedTheme);

    if (savedTheme === "light") {
        document.body.classList.add("light-mode");
        logo.src = lightLogo;
        logo.style.opacity = "1";
        logo.style.transform = "scale(1)";
        console.log("✅ Light mode actief, logo aangepast naar:", lightLogo);
    } else {
        document.body.classList.remove("light-mode");
        logo.src = darkLogo;
        logo.style.opacity = "1";
        logo.style.transform = "scale(1)";
        console.log("🌙 Dark mode actief, logo aangepast naar:", darkLogo);
    }

    
    // 🎨 Particles Effect
    let particles = [];

    class Particle {
        constructor(x, y, size, speedX, speedY, color) {
            this.x = x;
            this.y = y;
            this.size = size;
            this.speedX = speedX;
            this.speedY = speedY;
            this.color = color;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x > canvas.width || this.x < 0) this.speedX *= -1;
            if (this.y > canvas.height || this.y < 0) this.speedY *= -1;
        }

        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.fill();
            ctx.closePath();
        }
    }




    function initParticles() {
        particles = [];
        for (let i = 0; i < 100; i++) {
            let size = Math.random() * 3 + 1.5;
            let x = Math.random() * canvas.width;
            let y = Math.random() * canvas.height;
            let speedX = (Math.random() - 0.5) * 1.2;
            let speedY = (Math.random() - 0.5) * 1.2;

            let colors = ["#90caf9", "#64b5f6", "#4db6ac", "#81c784"];
            let color = colors[Math.floor(Math.random() * colors.length)];

            particles.push(new Particle(x, y, size, speedX, speedY, color));
        }
    }
    

    function animateParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });

        requestAnimationFrame(animateParticles);
    }

    // ✅ **Verplaats deze naar onder!**
    initParticles();
    animateParticles();
    const cards = document.querySelectorAll(".automation-card");

    cards.forEach(card => {
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            card.style.setProperty("--mouse-x", `${x}px`);
            card.style.setProperty("--mouse-y", `${y}px`);
        });
    });

});