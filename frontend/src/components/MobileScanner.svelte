<script>
  import { onMount, onDestroy } from 'svelte';
  import { initScanner } from '../lib/scanner';
  
  let scanner;
  let lastScanned = '';
  
  onMount(() => {
    scanner = initScanner(
      'scanner-container',
      handleScanSuccess,
      handleScanError
    );
  });
  
  onDestroy(() => {
    if (scanner) scanner.clear();
  });
  
  function handleScanSuccess(decodedText) {
    if (decodedText !== lastScanned) {
      lastScanned = decodedText;
      // Vibrar dispositivo si es soportado
      if (navigator.vibrate) navigator.vibrate(200);
      
      // Enviar a backend
      processScannedCode(decodedText);
    }
  }
  
  function handleScanError(error) {
    console.error('Error de escaneo:', error);
  }
  
  async function processScannedCode(code) {
    try {
      const response = await fetch('/api/v1/scan/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code })
      });
      
      const result = await response.json();
      showNotification(result);
    } catch (error) {
      console.error('Error al procesar código:', error);
    }
  }
  
  function showNotification(result) {
    // Usar notificaciones nativas
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(`Producto: ${result.product.name}`, {
        body: `Stock: ${result.currentStock}`,
        icon: '/icon-192x192.png'
      });
    }
  }
</script>

<div class="mobile-scanner">
  <div id="scanner-container" class="scanner-view" />
  
  <div class="scanner-controls">
    <button 
      on:click={() => scanner?.clear()}
      class="btn-stop"
    >
      Detener Escaneo
    </button>
  </div>
  
  <style>
    .mobile-scanner {
      position: relative;
      height: 100vh;
      width: 100vw;
    }
    
    .scanner-view {
      width: 100%;
      height: 100%;
    }
    
    .scanner-controls {
      position: absolute;
      bottom: 20px;
      left: 0;
      right: 0;
      text-align: center;
    }
    
    .btn-stop {
      background: rgba(255, 0, 0, 0.7);
      color: white;
      padding: 12px 24px;
      border-radius: 24px;
      border: none;
      font-size: 16px;
    }
  </style>
</div>
