document.addEventListener("DOMContentLoaded", function () {
    fetch("events.json")
        .then(response => response.json())
        .then(garbageData => {
            const today = new Date().toISOString().split("T")[0];

            const dateElement = document.getElementById("dateDisplay");
            console.log(dateElement);
            const bins = document.querySelectorAll(".bin img");

            const binImages = {
                "blau": "./images/Papiertonnen.jpg",
                "braun": "./images/Biotonne.jpg",
                "grau": "./images/Restmuell.jpg",
                "gelb": "./images/gelbtonne.jpg"
            };

            const todaysEntry = garbageData.find(entry => entry.start === today);

            if (todaysEntry) {
                dateElement.textContent = `Datum: ${todaysEntry.start}`;
                const words = todaysEntry.summary.toLowerCase().split(", ");
                const detectedBins = words
                    .map(word => Object.keys(binImages).find(key => word.includes(key)))
                    .filter(Boolean);

                bins[0].src = detectedBins[0] ? binImages[detectedBins[0]] : "";
                bins[0].style.display = detectedBins[0] ? "block" : "none";

                bins[1].src = detectedBins[1] ? binImages[detectedBins[1]] : "";
                bins[1].style.display = detectedBins[1] ? "block" : "none";
            } else {
                dateElement.textContent = "Datum: Keine Abholung";
                bins.forEach(bin => bin.style.display = "none");
            }
        })
        .catch(error => console.error("Error loading JSON:", error));
});
