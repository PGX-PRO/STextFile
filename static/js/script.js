const st = document.getElementById("st");
const uploadingT = document.getElementById("uploadingT");
const uploadingF = document.getElementById("uploadingF");
const sf = document.getElementById("sf");
const input = document.getElementById("textTx");
sf.classList.add("hover:cursor-pointer");

function copyLink() {
 const link = document.getElementById("link").href.replaceAll("https://", "");
 const input = document.createElement("input");
 input.value = link;
 document.body.appendChild(input);
 input.select();
 document.execCommand("copy");
 document.body.removeChild(input);
 alert("Copied URL: " + link);
 const mainLink = window.location.origin + window.location.pathname;
 let x;
 const hostname = window.location.hostname;
 if (hostname === "localhost" || hostname === "127.0.0.1") {
  x = "http";
 } else {
  x = "https";
 }
 const linkGo = `${x}://${mainLink.split("/").slice(0, -1).slice(-1)[0]}`;
 window.location.href = linkGo;
}

function choose(selectedBtn) {
 const notification = document.getElementById("showNotification");
 if (notification) {
  notification.style.display = "none";
 }
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
 uploadingT.textContent = "Uploading File...";
 const text = document.getElementById("textTx").value;
 if (!text.trim()) {
  alert("Por favor ingresa algún texto");
  return;
 }
 const encoder = new TextEncoder();
 const bytes = encoder.encode(text);
 const blob = new Blob([bytes], { type: "application/octet-stream" });
 const file = new File([blob], "texto.txt", {
  type: "application/octet-stream",
 });
 const formData = new FormData();
 formData.append("archivo", file);
 formData.append("expiry", "30");

 const subir = async (datos) => {
  const res = await fetch("/upload_text", {
   method: "POST",
   body: datos,
  });

  if (!res.ok) throw new Error("conexión fallida");
  const result = await res.json();
  if (!result.success) throw new Error("error en servidor");
  const encoded = encodeURIComponent(encodeURIComponent(result.files[0].url));
  window.location.href = `/?success=true&file_url=${encoded}&active_tab=text`;
 };
 try {
  await subir(formData);
 } catch {
  const base64 = btoa(unescape(encodeURIComponent(text)));
  const blob64 = new Blob([base64], { type: "text/plain" });
  const file64 = new File([blob64], "texto_base64.txt", {
   type: "text/plain",
  });
  const formData64 = new FormData();
  formData64.append("archivo", file64);
  formData64.append("expiry", "30");
  try {
   await subir(formData64);
  } catch (e) {
   alert("Error final: " + e.message);
  }
 }
}

function uploadFile(event) {
 event.preventDefault();
 uploadingF.textContent = "Uploading File...";
 setTimeout(() => {
  event.target.form.submit();
 }, 100);
}
