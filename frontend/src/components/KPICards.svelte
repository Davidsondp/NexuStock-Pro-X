<script>
  export let metrics = {
    totalSales: 0,
    avgTurnover: 0,
    topProduct: null,
    stockAlerts: 0
  };
</script>

<div class="kpi-grid">
  <div class="kpi-card">
    <h3>Ventas Totales</h3>
    <div class="value">${metrics.totalSales.toFixed(2)} HTG</div>
  </div>
  
  <div class="kpi-card">
    <h3>Rotación Promedio</h3>
    <div class="value">{metrics.avgTurnover.toFixed(2)}</div>
  </div>
  
  <div class="kpi-card">
    <h3>Producto Más Vendido</h3>
    <div class="value">{metrics.topProduct?.name || 'N/A'}</div>
  </div>
  
  <div class="kpi-card">
    <h3>Alertas de Stock</h3>
    <div class="value">{metrics.stockAlerts}</div>
  </div>
</div>
