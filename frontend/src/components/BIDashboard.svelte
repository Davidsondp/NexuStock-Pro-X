<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  
  let salesData = [];
  let turnoverData = [];
  let timeRange = '30d';
  let categoryFilter = '';
  let isLoading = false;
  
  onMount(async () => {
    await fetchAnalyticsData();
  });
  
  async function fetchAnalyticsData() {
    isLoading = true;
    try {
      const salesResponse = await fetch(`/api/v1/analytics/sales?time_range=${timeRange}&category=${categoryFilter}`);
      salesData = await salesResponse.json();
      
      const turnoverResponse = await fetch('/api/v1/analytics/inventory/turnover');
      turnoverData = await turnoverResponse.json();
      
      renderCharts();
    } finally {
      isLoading = false;
    }
  }
  
  function renderCharts() {
    renderSalesChart();
    renderTurnoverChart();
  }
  
  function renderSalesChart() {
    const ctx = document.getElementById('salesChart');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: salesData.map(d => new Date(d.date).toLocaleDateString()),
        datasets: [{
          label: 'Ventas Totales (HTG)',
          data: salesData.map(d => d.total_sales),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      }
    });
  }
  
  function renderTurnoverChart() {
    const ctx = document.getElementById('turnoverChart');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: turnoverData.map(d => d.name),
        datasets: [{
          label: 'Rotación de Inventario',
          data: turnoverData.map(d => d.turnover_rate),
          backgroundColor: 'rgba(54, 162, 235, 0.5)'
        }]
      }
    });
  }
</script>

<div class="bi-dashboard">
  <div class="filters">
    <select bind:value={timeRange}>
      <option value="7d">Últimos 7 días</option>
      <option value="30d">Últimos 30 días</option>
      <option value="90d">Últimos 90 días</option>
    </select>
    
    <button on:click={fetchAnalyticsData} disabled={isLoading}>
      {isLoading ? 'Cargando...' : 'Aplicar Filtros'}
    </button>
  </div>
  
  <div class="chart-container">
    <div class="chart">
      <h3>Trend de Ventas</h3>
      <canvas id="salesChart"></canvas>
    </div>
    
    <div class="chart">
      <h3>Rotación de Inventario</h3>
      <canvas id="turnoverChart"></canvas>
    </div>
  </div>
</div>
