<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto';
  
  let datosVentas = [];
  let datosRotacion = [];
  let rangoTiempo = '30d';
  let filtroCategoria = '';
  let cargando = false;
  
  onMount(async () => {
    await cargarDatosAnaliticos();
  });
  
  async function cargarDatosAnaliticos() {
    cargando = true;
    try {
      const respuestaVentas = await fetch(`/api/v1/analitica/ventas?rango_tiempo=${rangoTiempo}&categoria=${filtroCategoria}`);
      datosVentas = await respuestaVentas.json();
      
      const respuestaRotacion = await fetch('/api/v1/analitica/inventario/rotacion');
      datosRotacion = await respuestaRotacion.json();
      
      renderizarGraficos();
    } finally {
      cargando = false;
    }
  }
  
  function renderizarGraficos() {
    renderizarGraficoVentas();
    renderizarGraficoRotacion();
  }
  
  function renderizarGraficoVentas() {
    const ctx = document.getElementById('graficoVentas');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: datosVentas.map(d => new Date(d.fecha).toLocaleDateString()),
        datasets: [{
          label: 'Ventas Totales (HTG)',
          data: datosVentas.map(d => d.ventas_totales),
          borderColor: 'rgb(75, 192, 192)',
          tension: 0.1
        }]
      }
    });
  }
  
  function renderizarGraficoRotacion() {
    const ctx = document.getElementById('graficoRotacion');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: datosRotacion.map(d => d.nombre),
        datasets: [{
          label: 'Rotación de Inventario',
          data: datosRotacion.map(d => d.tasa_rotacion),
          backgroundColor: 'rgba(54, 162, 235, 0.5)'
        }]
      }
    });
  }
</script>

<div class="dashboard-bi">
  <div class="filtros">
    <select bind:value={rangoTiempo}>
      <option value="7d">Últimos 7 días</option>
      <option value="30d">Últimos 30 días</option>
      <option value="90d">Últimos 90 días</option>
    </select>
    
    <button on:click={cargarDatosAnaliticos} disabled={cargando}>
      {cargando ? 'Cargando...' : 'Aplicar Filtros'}
    </button>
  </div>
  
  <div class="contenedor-graficos">
    <div class="grafico">
      <h3>Tendencia de Ventas</h3>
      <canvas id="graficoVentas"></canvas>
    </div>
    
    <div class="grafico">
      <h3>Rotación de Inventario</h3>
      <canvas id="graficoRotacion"></canvas>
    </div>
  </div>
</div>
