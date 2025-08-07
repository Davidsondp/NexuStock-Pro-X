<script>
  let escuchando = false;
  let textoReconocido = "";
  
  function iniciarReconocimiento() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = "es-ES";  // Puede cambiarse dinámicamente
    
    recognition.onresult = (event) => {
      textoReconocido = event.results[0][0].transcript;
      enviarComando(textoReconocido);
    };
    
    recognition.start();
    escuchando = true;
  }
  
  async function enviarComando(texto) {
    const response = await fetch("/api/voz/procesar", {
      method: "POST",
      body: JSON.stringify({ comando: texto })
    });
    // Reproducir respuesta auditiva
    const audio = new Audio(await response.blob());
    audio.play();
  }
</script>

<button on:click={iniciarReconocimiento} disabled={escuchando}>
  {escuchando ? "Escuchando..." : "Hablar"}
</button>
<p>{textoReconocido || "Di algo..."}</p>
