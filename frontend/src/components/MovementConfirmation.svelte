<script>
  export let scanResult;
  export let quantity;
  export let movementType;
  export let onConfirm;
  export let onCancel;
  
  $: movementText = {
    'entrada': 'Entrada',
    'salida': 'Salida',
    'ajuste': 'Ajuste'
  }[movementType];
</script>

<div class="bg-white p-4 rounded-lg shadow">
  <h2 class="text-lg font-bold mb-4">Confirmar Movimiento</h2>
  
  <div class="space-y-3">
    <div>
      <span class="font-semibold">Producto:</span> {scanResult.product?.name || 'Cargando...'}
    </div>
    
    <div>
      <span class="font-semibold">Tipo:</span> {movementText}
    </div>
    
    <div>
      <span class="font-semibold">Cantidad:</span> {quantity}
    </div>
    
    {#if scanResult.product}
      <div class="grid grid-cols-2 gap-4 mt-4">
        <div class="bg-gray-100 p-3 rounded">
          <div class="text-sm text-gray-500">Stock Actual</div>
          <div class="text-xl font-bold">{scanResult.product.current_stock}</div>
        </div>
        <div class="bg-blue-50 p-3 rounded">
          <div class="text-sm text-blue-500">Nuevo Stock</div>
          <div class="text-xl font-bold text-blue-700">
            {scanResult.product.new_stock}
          </div>
        </div>
      </div>
    {/if}
  </div>
  
  <div class="flex justify-end space-x-3 mt-6">
    <button 
      on:click={onCancel}
      class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
    >
      Cancelar
    </button>
    <button 
      on:click={onConfirm}
      class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
    >
      Confirmar
    </button>
  </div>
</div>
