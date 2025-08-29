// Update the date and time for misc-text
const miscText = document.querySelector(".misc-text");
const nodeContent = document.createElement("p");
const date = new Date();
nodeContent.textContent = "SOICT 2025, " + date.getDay() + "/" + date.getMonth() + "/" + date.getFullYear() + ", " + "Ho Chi Minh City, Vietnam"
miscText.appendChild(nodeContent)

/**
 * Shows the Bootstrap alert-danger component with a custom message for 2 seconds.
 * @param {string} message - The custom text to display in the alert.
 */
function showAlertDanger(message) {
    // Select the alert element
    const alertEl = document.querySelector('.alert-danger');
    if (!alertEl) {
        return;
    }

    // Find the text node (skip the SVG and button)
    // The alert structure: [SVG, textNode, button]
    // We'll update the text node (nodeType === 3)
    let textNode = null;
    for (let node of alertEl.childNodes) {
        if (node.nodeType === 3 && node.textContent.trim() !== "") {
            textNode = node;
            break;
        }
    }
    if (textNode) {
        textNode.textContent = " " + message + " ";
    }

    // Show the alert (remove d-none if present)
    alertEl.classList.remove('d-none');
    // Add Bootstrap's 'show' class if not present
    alertEl.classList.add('show');

    // Hide the alert after 2 seconds (2000 ms)
    setTimeout(() => {
        // Add d-none to hide, remove show for Bootstrap fade
        alertEl.classList.add('d-none');
        alertEl.classList.remove('show');
    }, 2000);
}


// Fetch server / Search logic
const teamTitle = document.getElementsByClassName("team-title")[0];
const inputField = document.getElementsByClassName("query-input")[0];
const searchMenu = document.getElementsByClassName("search-menu")[0];
const filterContainer = document.getElementsByClassName("filter-container")[0];
const spinner = document.getElementsByClassName("query-spinner")[0];
const imageContainer = document.getElementsByClassName("image-container")[0];
const template = document.getElementById('card-template').content;

if (!imageContainer || !spinner || !filterContainer || !searchMenu || !inputField || !teamTitle)
    showAlertDanger("An unexpected error occurred")


const fetchEndpoint = "http://localhost:5000/search"

inputField.addEventListener("keyup", function (event) {
    if (event.key === "Enter") {
        if (event.target.value === "") {
            showAlertDanger("Value field can't be empty")
            return;
        }

        if (event.target.value.length < 3) {
            showAlertDanger("Please search more than 3 characters")
            return;
        }

        teamTitle.classList.add("collapsed")
        filterContainer.classList.remove("justify-content-center")
        spinner.classList.remove("d-none");

        // Mock query
        const fetchEndpointFn = async () => {
            try {
                const response = await fetch(`${fetchEndpoint}?searchType=test&q=${event.target.value}`);
                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }

                const { result: results } = await response.json();

                // Clear previous results for better UX
                imageContainer.innerHTML = "";

                // Use forEach for better readability and performance
                // Assuming 'results' is an array of image URLs
                if (Array.isArray(results)) {
                    results.forEach(({ url, id }) => {
                        const imgCard = document.importNode(template, true);
                        const imgLink = imgCard.querySelector(".video-link");

                        if (imgLink) {
                            imgLink.textContent = url.split("/")[4] + "/" + url.split("/")[5];
                            imgLink.href = `https://drive.google.com/file/d/${id}/preview`;
                        }

                        // querySelector returns the first matching element, so no [0] needed
                        const imgElement = imgCard.querySelector("img");
                        if (imgElement) {
                            imgElement.src = url;
                        }
                        imageContainer.appendChild(imgCard);
                    });
                } else {
                    console.warn("Results is not an array:", results);
                }
            } catch (error) {
                console.error("Fetch error:", error.message);
            }
        }

        fetchEndpointFn();
        spinner.classList.add("d-none");
    }
});
