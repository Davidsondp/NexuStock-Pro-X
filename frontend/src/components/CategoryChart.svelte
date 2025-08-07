<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  
  let chart;
  let categories = [];
  
  onMount(async () => {
    const response = await fetch('/api/v1/products/category-distribution');
    const data = await response.json();
    categories = data;
    renderChart();
  });
  
  function renderChart() {
    const ctx = document.getElementById('categoryChart');
    
    if (chart) chart.destroy();
    
    chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: categories.map(c => c.category),
        datasets: [{
          data: categories.map(c => c.count),
          backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', 
            '#9966FF', '#FF9F40', '#8AC24A', '#607D8B'
          ]
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'right'
          }
        }
      }
    });
  }
</script>

<div class="bg-white p-4 rounded-lg shadow">
  <h2 class="text-lg font-semibold mb-4">Distribución por Categoría</h2>
  <div class="h-64">
    <canvas id="categoryChart"></canvas>
  </div>
</div>
