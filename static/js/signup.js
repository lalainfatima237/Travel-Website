document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("signupForm");

    if (form) {
        form.addEventListener("submit", async function (e) {
            e.preventDefault();

            // 1. Sab data collect karein (Ensure IDs match your HTML inputs)
            const formData = {
                username: document.querySelector("input[placeholder*='name']").value,
                email: document.querySelector("input[type='email']").value,
                password: document.querySelector("input[type='password']").value,
                address: document.querySelector("input[placeholder*='address']")?.value || "",
                cnic: document.getElementById("cnic").value,
            };

            // 2. CSRF Token get karein (Django requires this for POST)
            // Note: Make sure to add <script>const CSRF_TOKEN = "{{ csrf_token }}";</script> in your HTML
            const csrfToken = typeof CSRF_TOKEN !== 'undefined' ? CSRF_TOKEN : "";

            try {
                // 3. API Request bhejein
                const response = await fetch("/api/signup/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": csrfToken
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();

                if (response.ok) {
                    // Success! Redirect to login
                    alert("Registration Successfully!");
                    window.location.href = "/login/"; 
                } else {
                    // Backend validation errors (e.g., username already exists)
                    console.error("Validation Errors:", data);
                    let errorMsg = "";
                    for (let key in data) {
                        errorMsg += `${key}: ${data[key]}\n`;
                    }
                    alert("Signup Failed:\n" + errorMsg);
                }
            } catch (error) {
                console.error("Network Error:", error);
                alert("Server se connection nahi ho saka. Terminal check karein.");
            }
        });
    } else {
        console.error("Error: Form with ID 'signupForm' not found! Please check your HTML tag.");
    }
});