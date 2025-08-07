export function formatearMoneda(monto, moneda = "HTG") {
  const opciones = {
    style: "currency",
    currency: moneda,
    minimumFractionDigits: 2,
  };

  if (moneda === "HTG") {
    return `G ${monto.toFixed(2)}`;  // Formato: G 1,200.50
  }
  return new Intl.NumberFormat("es-ES", opciones).format(monto);
}
