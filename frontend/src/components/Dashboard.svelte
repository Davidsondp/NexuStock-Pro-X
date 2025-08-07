<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  import DashboardCard from './DashboardCard.svelte';
  
  let dashboardData = null;
  let movementTrends = [];
  let chart = null;
  
  onMount(async () => {
    await fetchDashboardData();
    await fetchMovementTrends();
  });
  
  async function fetchDashboardData() {
    const response = await fetch('/api/v1/dashboard');
    dashboardData = await response.json();
  }
  
  async function fetchMovementTrends() {
    const response = await fetch('/api/v1/dashboard/movement-trends?days=30');
    movementTrends = await response.json();
    renderChart();
  }
  
  function renderChart() {
    const ctx = document.getElementById('movementChart');
    
    if (chart) chart.destroy();
    
    // Procesar datos para el gráfico
    const dates = [...new Set(movementTrends.map(m => m.date))].sort();
    const inflows = dates.map(date => {
      const entry = movementTrends.find(m => m.date === date && m.type === 'in');
      return entry ? entry.total : 0;
    });
    
    const outflows = dates.map(date => {
      const entry = movementTrends.find(m => m.date === date && m.type === 'out');
      return entry ? entry.total : 0;
    });
    
    chart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Entradas',
            data: inflows,
            backgroundColor: 'rgba(75, 192, 192, 0.7)'
          },
          {
            label: 'Salidas',
            data: outflows,
            backgroundColor: 'rgba(255, 99, 132, 0.7)'
          }
        ]
      },
      options: {
        responsive: true,
        scales: {
          x: { stacked: true },
          y: { stacked: true }
        }
      }
    });
  }
</script>

<div class="space-y-6">
  <!-- Tarjetas resumen -->
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <DashboardCard 
      title="Productos Totales" 
      value={dashboardData?.total_products}
      icon="📦"
    />
    <DashboardCard 
      title="Bajo Stock" 
      value={dashboardData?.low_stock_items}
      icon="⚠️"
      alert={dashboardData?.low_stock_items > 0}
    />
    <DashboardCard 
      title="Valor Inventario (HTG)" 
      value={dashboardData?.total_inventory_value_htg?.toLocaleString()}
      icon="💰"
    />
    <DashboardCard 
      title="Movimientos Hoy" 
      value={dashboardData?.movements_today}
      icon="🔄"
    />
  </div>
  
  <!-- Gráfico de tendencias -->
  <div class="bg-white p-4 rounded-lg shadow">
    <h2 class="text-lg font-semibold mb-4">Tendencias de Movimientos (Últimos 30 días)</h2>
    <div class="h-80">
      <canvas id="movementChart"></canvas>
    </div>
  </div>
  
  <!-- Productos con bajo stock -->
  {#if dashboardData?.low_stock_items > 0}
    <div class="bg-white p-4 rounded-lg shadow">
      <h2 class="text-lg font-semibold mb-4">Productos con Stock Bajo</h2>
      <LowStockProductsList />
    </div>
  {/if}
</div>
