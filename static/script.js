// DOM Element Selection
const uploadForm = document.getElementById("upload-form");
const fileInput = document.getElementById("file-input");
const fileNameDisplay = document.getElementById("file-name");
const loader = document.querySelector(".loader");
const resultContainer = document.getElementById("result-container");
const asciiArtContainer = document.getElementById("ascii-art");
const copyBtn = document.getElementById("copy-btn");
const downloadBtn = document.getElementById("download-btn");

/**
 * Displays the name of the selected file and stores it.
 */
function updateFileName() {
	if (fileInput.files.length > 0) {
		const filename = fileInput.files[0].name;
		fileNameDisplay.textContent = filename;
	}
	else {
		fileNameDisplay.textContent = "";
	}
}

/**
 * Submits the form data asynchronously to generate ASCII art.
 * @param {Event} event - The form submission event.
 */
function handleFormSubmit(event) {
	event.preventDefault(); // Prevent the default page reload

	if (fileInput.files.length === 0) {
		alert("Please select an image file first.");
		return;
	}

	// Show loader and hide previous result
	resultContainer.style.display = "none";
	loader.style.display = "block";

	const formData = new FormData(uploadForm);

	fetch("/upload", {
		method: "POST",
		body: formData,
	})
		.then((response) => {
			if (!response.ok) {
				return response
					.text()
					.then((text) => Promise.reject(text || "Server error"));
			}
			return response.json();
		})
		.then((data) => {
			const asciiText = data.art.join("\n");
			asciiArtContainer.textContent = asciiText;
			resultContainer.style.display = "block";
		})
		.catch((error) => {
			console.error("Error:", error);
			alert("An error occurred: " + error);
		})
		.finally(() => {
			// Always hide the loader, whether it succeeded or failed
			loader.style.display = "none";
		});
}

/**
 * Copies the ASCII art result to the clipboard.
 */
function copyToClipboard() {
	const textToCopy = asciiArtContainer.textContent;
	navigator.clipboard
		.writeText(textToCopy)
		.then(() => {
			const originalText = copyBtn.textContent;
			copyBtn.textContent = "Copied!";
			setTimeout(() => {
				copyBtn.textContent = originalText;
			}, 2500);
		})
		.catch((err) => {
			console.error("Failed to copy text: ", err);
			alert("Failed to copy text.");
		});
}

/**
 * Triggers a download of the ASCII art as a .txt file.
 */
function downloadAsText() {
	// Get the filename stem (remove the last extension)
	const originalFilename = fileNameDisplay.textContent
	const nameParts = originalFilename.split(".");
	const stem =
		nameParts.length > 1 ? nameParts.slice(0, -1).join(".") : originalFilename;
	const newFilename = `${stem}_ascii-art-ified.txt`;

	const textToDownload = asciiArtContainer.textContent;
	const blob = new Blob([textToDownload], { type: "text/plain" });
	const url = URL.createObjectURL(blob);
	const a = document.createElement("a");
	a.href = url;
	a.download = newFilename; // Use the new, dynamic filename
	document.body.appendChild(a);
	a.click();
	document.body.removeChild(a);
	URL.revokeObjectURL(url);
}

/**

 * Attaches event listeners to the interactive elements.
 */
function initialize() {
	if (uploadForm) uploadForm.addEventListener("submit", handleFormSubmit);
	if (fileInput) fileInput.addEventListener("change", updateFileName);
	if (copyBtn) copyBtn.addEventListener("click", copyToClipboard);
	if (downloadBtn) downloadBtn.addEventListener("click", downloadAsText);
}

// Start the application
initialize();
