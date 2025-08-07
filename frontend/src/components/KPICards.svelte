<script>
  export let metricas = {
    ventasTotales: 0,
    rotacionPromedio: 0,
    productoTop: null,
    alertasStock: 0
  };
</script>

<div class="grid-kpi">
  <div class="tarjeta-kpi">
    <h3>Ventas Totales</h3>
    <div class="valor">${metricas.ventasTotales.toFixed(2)} HTG</div>
  </div>
  
  <div class="tarjeta-kpi">
    <h3>Rotación Promedio</h3>
    <div class="valor">{metricas.rotacionPromedio.toFixed(2)}</div>
  </div>
  
  <div class="tarjeta-kpi">
    <h3>Producto Más Vendido</h3>
    <div class="valor">{metricas.productoTop?.nombre || 'N/A'}</div>
  </div>
  
  <div class="tarjeta-kpi">
    <h3>Alertas de Stock</h3>
    <div class="valor">{metricas.alertasStock}</div>
  </div>
</div>
