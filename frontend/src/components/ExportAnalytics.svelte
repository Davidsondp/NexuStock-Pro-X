<script>
  let exportFormat = 'csv';
  let includeCharts = false;
  
  async function exportData() {
    const params = new URLSearchParams({
      format: exportFormat,
      charts: includeCharts
    });
    
    window.open(`/api/v1/analytics/export?${params.toString()}`, '_blank');
  }
</script>

<div class="export-panel">
  <h3>Exportar Datos Analíticos</h3>
  
  <div>
    <label>
      <input type="radio" bind:group={exportFormat} value="csv" />
      CSV
    </label>
    <label>
      <input type="radio" bind:group={exportFormat} value="excel" />
      Excel
    </label>
  </div>
  
  <button on:click={exportData}>
    Generar Reporte
  </button>
</div>
