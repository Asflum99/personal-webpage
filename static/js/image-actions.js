function getCSRFTokenFromCookie() {
  const name = "csrftoken";
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith(name + "=")) {
      return decodeURIComponent(cookie.substring(name.length + 1));
    }
  }
  return null;
}

function deleteImage(filename, safeId) {
  if (!confirm("¿Estás seguro de que quieres eliminar esta imagen?")) return;

  const formData = new FormData();
  formData.append("filename", filename);

  fetch("/delete_image/", {
    method: "POST",
    body: formData,
    headers: {
      "X-CSRFToken": getCSRFTokenFromCookie(),
    },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        alert("Error: " + data.error);
        return;
      }

      const imageDiv = document.getElementById("img-" + safeId);
      if (imageDiv) {
        imageDiv.remove();
      }

      if (document.querySelectorAll('[id^="img-"]').length === 0) {
        window.close();
      }
    })
    .catch((error) => alert("Error al eliminar la imagen: " + error));
}

function uploadImage() {
  document
    .getElementById("upload-form")
    .addEventListener("submit", function (e) {
      e.preventDefault();
      const fileInput = document.getElementById("image-upload");
      const file = fileInput.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      fetch("/upload_image/", {
        method: "POST",
        body: formData,
        headers: {
          "X-CSRFToken": getCSRFTokenFromCookie(),
        },
      })
        .then((res) => res.json())
        .then((json) => {
          if (json.location) {
            window.opener.postMessage(
              { url: json.location, title: file.name },
              "*"
            );
          } else {
            alert("Error al subir la imagen.");
          }
        })
        .catch(() => alert("Error en la conexión con el servidor."));
    });
}

function assignDeleteHandlers() {
  document.querySelectorAll(".delete-image-btn").forEach((btn) => {
    btn.addEventListener("click", function (e) {
      const filename = btn.getAttribute("data-filename");
      const safeId = btn.getAttribute("data-safeid");
      deleteImage(filename, safeId);
    });
  });
}

