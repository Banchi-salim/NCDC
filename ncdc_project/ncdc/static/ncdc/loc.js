document.addEventListener("DOMContentLoaded", () => {
    // Check if the page title is "Home - NCDC"
    if (document.title === "Home - NCDC") {
        if (navigator.geolocation) {
            // Check if the location permission is already granted or prompt
            navigator.permissions.query({ name: "geolocation" }).then((result) => {
                if (result.state === "granted" || result.state === "prompt") {
                    // Retrieve location on page load with high accuracy options
                    navigator.geolocation.getCurrentPosition(
                        (position) => {
                            // Swap longitude and latitude, pass with high accuracy settings
                            const longitude = position.coords.latitude;
                            const latitude = position.coords.longitude;
                            const accuracy = position.coords.accuracy;

                            console.log(`Coordinates: ${longitude}, ${latitude}`);
                            console.log(`Accuracy: ${accuracy} meters`);
                            sendLocationToServer(longitude, latitude);
                        },
                        (error) => {
                            alert("Unable to access location. Location access is required for personalized alerts.");
                        },
                        {
                            enableHighAccuracy: true,
                            timeout: 10000,
                            maximumAge: 0
                        }
                    );
                } else {
                    alert("Location access is required for personalized alerts.");
                }
            });
        } else {
            alert("Geolocation is not supported by your browser.");
        }
    }
});

function sendLocationToServer(lat, lng) {
    fetch("update-location/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify({
            latitude: lat,
            longitude: lng
        }),
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        // Display the alert message from the server
        if (data.alert) {
            alert(data.alert);
        }
    })
    .catch((error) => {
        console.error("Error sending location:", error);
        alert("An error occurred while checking for disease outbreaks.");
    });
}

// Utility function to retrieve CSRF token
function getCsrfToken() {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    return csrfToken ? csrfToken.value : "";
}