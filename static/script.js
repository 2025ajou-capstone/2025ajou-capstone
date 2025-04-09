const dropZone = document.getElementById("drop-zone");
const preview = document.getElementById("preview");

dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("hover");
});

dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("hover");
});

dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("hover");

    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
        upload(file);
    } else {
        alert("이미지 파일만 가능합니다.");
    }
});

function upload(file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        preview.innerHTML = `
            <p>인식된 차량 번호: <strong>${data.plate_number}</strong></p>
            <img src="/media/${file.name}" alt="preview"/>
        `;
    })
    .catch(err => {
        alert("업로드 실패: " + err);
    });
}