window.initializeImagePicker = function (callback, value, meta) {
  if (meta.filetype === "image") {
    fetch("/image_list/")
      .then((response) => response.json())
      .then((data) => handleImageListResponse(data, callback));
  }
};

function handleImageListResponse(data, callback) {
  if (data.empty) {
    alert("No hay imágenes en la base de datos");
    return;
  }

  const win = createImagePickerWindow();
  renderImageList(win, data, callback);
  setupMessageListener(win, callback);
}

function createImagePickerWindow() {
  const win = window.open("", "Galería de imágenes", "width=800,height=600");
  win.document.writeln('<div style="padding: 20px;">');
  return win;
}

function renderImageList(win, data, callback) {
  let html = `
    <h3>Selecciona una imagen</h3>

    <!-- 🖼 Formulario para subir nueva imagen -->
    <form id="upload-form" style="margin-bottom: 20px;">
      <input type="file" id="image-upload" accept="image/*" required>
      <button type="submit">Subir nueva imagen</button>
    </form>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 10px;">
  `;

  data.images.forEach((image) => {
    html += createImageElement(image);
  });

  html += `
    </div>
    <script>
      const script = document.createElement('script');
      script.src = "/static/js/image-actions.js";
      script.onload = function() {
        if (typeof uploadImage === "function") {
          uploadImage();
        }
        if (typeof assignDeleteHandlers === "function") {
          assignDeleteHandlers();
        }
      };
      document.body.appendChild(script);
    <\/script>
  `;

  win.document.writeln(html);
}

function createImageElement(image) {
  return `
        <div id="img-${image.safe_id}" style="cursor: pointer; text-align: center; position: relative;">
            <div onclick="window.opener.postMessage({url: '${image.url}', title: '${image.text}'}, '*')">
                <img src="${image.url}" 
                     style="max-width: 100%; height: auto; margin-bottom: 5px;">
                <div>${image.text}</div>
            </div>
            <button class="delete-image-btn"
                    data-filename="${image.text}"
                    data-safeid="${image.safe_id}"
                    style="position: absolute; top: 5px; right: 5px; 
                          background: red; color: white; border: none; 
                          border-radius: 50%; width: 24px; height: 24px; 
                          cursor: pointer;">×</button>
        </div>
    `;
}

function setupMessageListener(win, callback) {
  window.addEventListener(
    "message",
    function (e) {
      callback(e.data.url, { title: e.data.title });
      win.close();
    },
    { once: true }
  );
}
