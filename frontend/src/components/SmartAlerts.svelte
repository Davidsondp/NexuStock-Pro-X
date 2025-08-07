<script>
  import { onMount } from 'svelte';
  
  let alerts = [];
  let isLoading = false;
  
  async function fetchAlerts() {
    isLoading = true;
    try {
      const response = await fetch('/api/v1/ai/stock-alerts');
      alerts = await response.json();
    } finally {
      isLoading = false;
    }
  }
  
  onMount(fetchAlerts);
</script>

<div class="bg-white p-6 rounded-lg shadow">
  <div class="flex justify-between items-center mb-4">
    <h2 class="text-xl font-bold">Alertas Inteligentes</h2>
    <button 
      on:click={fetchAlerts}
      class="px-3 py-1 bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200"
    >
      Actualizar
    </button>
  </div>
  
  {#if isLoading}
    <div class="text-center py-8">Cargando alertas...</div>
  {:else if alerts.length === 0}
    <div class="text-center py-8 text-green-600">
      ✅ No hay alertas críticas
    </div>
  {:else}
    <div class="space-y-4">
      {#each alerts as alert}
        <div class="border-l-4 ${
          alert.prediction.recommendation.action === 'urgent_order' ? 'border-red-500' : 
          'border-yellow-500'
        } pl-4 py-2">
          <div class="flex justify-between">
            <h3 class="font-medium">{alert.product.name.es}</h3>
            <span class="text-sm ${
              alert.prediction.recommendation.action === 'urgent_order' ? 'text-red-600' : 
              'text-yellow-600'
            }">
              {alert.prediction.recommendation.message}
            </span>
          </div>
          
          <div class="grid grid-cols-3 gap-4 mt-2 text-sm">
            <div>
              <span class="text-gray-500">Stock actual:</span> {alert.product.current_stock}
            </div>
            <div>
              <span class="text-gray-500">Proyección mínima:</span> {Math.min(...alert.prediction.stock_projection).toFixed(2)}
            </div>
            <div>
              <span class="text-gray-500">Sugerencia:</span> {alert.prediction.recommendation.quantity.toFixed(2)} unidades
            </div>
          </div>
        </div>
      {/each}
    </div>
  {/if}
</div>
