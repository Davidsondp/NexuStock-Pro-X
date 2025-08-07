<script>
  import { QrScanner } from './QrScanner';
  import MovementConfirmation from './MovementConfirmation.svelte';
  
  let scanner;
  let scanResult = null;
  let quantity = 1;
  let movementType = 'entrada';
  let isScanning = false;
  
  function handleScan(code) {
    scanResult = { barcode: code };
    isScanning = false;
  }
  
  async function confirmMovement() {
    const response = await fetch('/api/v1/movements/scan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        barcode: scanResult.barcode,
        quantity,
        type: movementType
      })
    });
    
    if (response.ok) {
      alert('Movimiento registrado!');
      scanResult = null;
    } else {
      alert(await response.text());
    }
  }
</script>

<div class="space-y-4">
  {#if !scanResult}
    <div class="flex space-x-4">
      <select bind:value={movementType} class="border p-2 rounded">
        <option value="entrada">Entrada</option>
        <option value="salida">Salida</option>
        <option value="ajuste">Ajuste</option>
      </select>
      
      <input 
        type="number" 
        bind:value={quantity}
        min="1"
        class="border p-2 rounded w-20"
      >
      
      <button 
        on:click={() => isScanning = true}
        class="bg-blue-500 text-white p-2 rounded"
      >
        Escanear Código
      </button>
    </div>
    
    {#if isScanning}
      <div class="border rounded-lg overflow-hidden">
        <QrScanner onScan={handleScan} />
        <button 
          on:click={() => isScanning = false}
          class="bg-red-500 text-white p-2 w-full"
        >
          Cancelar
        </button>
      </div>
    {/if}
  {:else}
    <MovementConfirmation 
      {scanResult}
      {quantity}
      {movementType}
      onConfirm={confirmMovement}
      onCancel={() => scanResult = null}
    />
  {/if}
</div>
