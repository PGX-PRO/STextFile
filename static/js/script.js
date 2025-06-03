const st = document.getElementById("st");
const sf = document.getElementById("sf");
sf.classList.add("hover:cursor-pointer");

function copyLink() {
  const link = document.getElementById("link").href;
  const input = document.createElement("input");
  input.value = link;
  document.body.appendChild(input);
  input.select();
  document.execCommand("copy");
  document.body.removeChild(input);
  alert("URL copiada: " + link);
}

function choose(selectedBtn) {
  const textSection = document.getElementById("textSection");
  const formx = document.getElementById("formx");
  st.classList.remove("bg-green-500", "text-white");
  st.classList.add("text-black");
  sf.classList.remove("bg-green-500", "text-white");
  sf.classList.add("text-black");
  selectedBtn.classList.add("bg-green-500", "text-white");
  selectedBtn.classList.remove("text-black");

  if (selectedBtn.id === "st") {
    textSection.classList.remove("hidden");
    formx.classList.add("hidden");
    st.classList.remove("hover:cursor-pointer");
    sf.classList.add("hover:cursor-pointer");
  } else {
    textSection.classList.add("hidden");
    formx.classList.remove("hidden");
    st.classList.add("hover:cursor-pointer");
    sf.classList.remove("hover:cursor-pointer");
  }
}

async function uploadText() {
  const text = document.getElementById("textTx").value;
  if (!text.trim()) {
    alert("Por favor ingresa algún texto");
    return;
  }

  const blob = new Blob([text], { type: "text/plain" });
  const file = new File([blob], "texto.txt", { type: "text/plain" });
  const formData = new FormData();
  formData.append("archivo", file);
  formData.append("expiry", "30");

  try {
    const response = await fetch("/upload_text", {
      method: "POST",
      body: formData,
    });

    if (response.ok) {
      const result = await response.json();
      if (result.success) {
        window.location.href = `/?success=true&file_url=${encodeURIComponent(
          result.files[0].url
        )}&active_tab=text`;
      } else {
        alert("Error al subir el archivo de texto");
      }
    } else {
      alert("Error en la conexión");
    }
  } catch (error) {
    alert("Error: " + error.message);
  }
}
