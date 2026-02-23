document.addEventListener("DOMContentLoaded", function () {
	const form = document.getElementById("upload-form");
	const fileInput = document.getElementById("file-input");
	const fileNameDisplay = document.getElementById("file-name");
	const loader = document.getElementById("loader");
	const resultContainer = document.getElementById("result-container");
	const asciiArtContainer = document.getElementById("ascii-art");
	const copyBtn = document.getElementById("copy-btn");
	const downloadBtn = document.getElementById("download-btn");

	// Update the file name display when a file is chosen
	fileInput.addEventListener("change", function () {
		if (fileInput.files.length > 0) {
			fileNameDisplay.textContent = fileInput.files[0].name;
		} else {
			fileNameDisplay.textContent = "";
		}
	});

	form.addEventListener("submit", function (event) {
		event.preventDefault(); // Prevent the default page reload

		if (fileInput.files.length === 0) {
			alert("Please select an image file first.");
			return;
		}

		// Hide previous result and show the loader
		resultContainer.style.display = "none";
		loader.style.display = "block";

		const formData = new FormData(form);

		// Use the Fetch API to send the form data asynchronously
		fetch("/upload", {
			method: "POST",
			body: formData,
		})
			.then((response) => {
				if (!response.ok) {
					// If the server response is not OK, throw an error to be caught by the .catch block
					return response.text().then((text) => {
						throw new Error(text || "Server responded with an error");
					});
				}
				return response.json(); // Parse the JSON response from the server
			})
			.then((data) => {
				// Hide the loader and show the result
				loader.style.display = "none";
				const asciiText = data.art.join("\n");
				asciiArtContainer.textContent = asciiText;
				resultContainer.style.display = "block";
			})
			.catch((error) => {
				// Hide the loader and show an error message
				loader.style.display = "none";
				console.error("Error:", error);
				alert("An error occurred: " + error.message);
			});
	});

	// --- New: Functionality for Copy and Download buttons ---
	copyBtn.addEventListener("click", function () {
		const textToCopy = asciiArtContainer.textContent;
		navigator.clipboard
			.writeText(textToCopy)
			.then(() => {
				// Provide user feedback
				const originalText = copyBtn.textContent;
				copyBtn.textContent = "Copied!";
				setTimeout(() => {
					copyBtn.textContent = originalText;
				}, 2000);
			})
			.catch((err) => {
				console.error("Failed to copy text: ", err);
				alert("Failed to copy text. Please try again.");
			});
	});

	downloadBtn.addEventListener("click", function () {
		const textToDownload = asciiArtContainer.textContent;
		const blob = new Blob([textToDownload], { type: "text/plain" });
		const url = URL.createObjectURL(blob);
		const a = document.createElement("a");
		a.href = url;
		a.download = "ascii-art.txt"; // The default filename for the download
		document.body.appendChild(a);
		a.click();
		document.body.removeChild(a);
		URL.revokeObjectURL(url);
	});
});
