<script>
  export let precioHtg;
  export let moneda = "USD";
  
  let precioConvertido = null;
  
  async function convertir() {
    const respuesta = await fetch(`/api/convertir?monto=${precioHtg}&origen=HTG&destino=${moneda}`);
    const datos = await respuesta.json();
    precioConvertido = datos.monto_convertido;
  }
</script>

<div>
  {#if precioConvertido}
    <p>{precioConvertido.toFixed(2)} {moneda}</p>
  {:else}
    <p>{precioHtg} HTG</p>
    <button on:click={convertir}>
      Convertir a {moneda}
    </button>
  {/if}
</div>
