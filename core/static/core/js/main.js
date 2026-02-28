const dropArea = document.getElementById("drop-area");
const fileInput = document.getElementById("fileInput");
const browseBtn = document.getElementById("browseBtn");
const fileInfo = document.getElementById("fileInfo");
const metadataForm = document.getElementById("metadataForm");

browseBtn.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", (e) => {
    handleFile(e.target.files[0]);
});

dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.boxShadow = "0 0 40px #00f5ff";
});

dropArea.addEventListener("dragleave", () => {
    dropArea.style.boxShadow = "none";
});

dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    fileInfo.classList.remove("hidden");
    fileInfo.innerHTML = `Uploaded: <strong>${file.name}</strong>`;
    metadataForm.classList.remove("hidden");
}