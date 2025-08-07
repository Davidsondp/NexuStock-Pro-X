<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  
  let productId = '';
  let days = 30;
  let prediction = null;
  let isLoading = false;
  let chart = null;
  
  async function getPrediction() {
    isLoading = true;
    try {
      const response = await fetch(`/api/v1/ai/predict-demand/${productId}?days=${days}`);
      prediction = await response.json();
      renderChart();
    } finally {
      isLoading = false;
    }
  }
  
  function renderChart() {
    const ctx = document.getElementById('predictionChart');
    
    if (chart) chart.destroy();
    
    const labels = Array.from({length: days}, (_, i) => `Día ${i+1}`);
    
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Stock Proyectado',
            data: prediction.stock_projection,
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.3
          },
          {
            label: 'Demanda Diaria',
            data: prediction.predictions,
            borderColor: '#EF4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            borderDash: [5, 5],
            fill: false
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Proyección de Stock (30 días)'
          },
          tooltip: {
            mode: 'index',
            intersect: false
          }
        },
        scales: {
          y: {
            beginAtZero: false
          }
        }
      }
    });
  }
</script>

<div class="bg-white p-6 rounded-lg shadow space-y-6">
  <h2 class="text-xl font-bold">Predicción de Demanda</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">Código de Producto</label>
      <input
        type="text"
        bind:value={productId}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      />
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Días a predecir</label>
      <input
        type="number"
        bind:value={days}
        min="7"
        max="90"
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      />
    </div>
    
    <div class="flex items-end">
      <button
        on:click={getPrediction}
        disabled={!productId || isLoading}
        class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Prediciendo...' : 'Predecir'}
      </button>
    </div>
  </div>
  
  {#if prediction}
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="bg-blue-50 p-4 rounded-lg">
        <h3 class="font-medium text-blue-800">Recomendación</h3>
        <p class="mt-2 text-lg ${
          prediction.recommendation.action === 'urgent_order' ? 'text-red-600' : 
          prediction.recommendation.action === 'order' ? 'text-yellow-600' : 
          'text-green-600'
        }">
          {prediction.recommendation.message}
        </p>
        {#if prediction.recommendation.quantity > 0}
          <p class="mt-1 text-sm">Cantidad sugerida: {prediction.recommendation.quantity.toFixed(2)}</p>
        {/if}
      </div>
      
      <div class="bg-gray-50 p-4 rounded-lg">
        <h3 class="font-medium text-gray-800">Stock Actual</h3>
        <p class="mt-2 text-2xl font-bold">{prediction.stock_projection[0]}</p>
      </div>
      
      <div class="bg-gray-50 p-4 rounded-lg">
        <h3 class="font-medium text-gray-800">Día Crítico</h3>
        <p class="mt-2 text-2xl font-bold">
          {prediction.critical_day ? `Día ${prediction.critical_day}` : 'No aplica'}
        </p>
      </div>
    </div>
    
    <div class="h-96">
      <canvas id="predictionChart"></canvas>
    </div>
  {/if}
</div>
