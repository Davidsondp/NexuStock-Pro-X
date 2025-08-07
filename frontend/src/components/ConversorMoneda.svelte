<script>
  export let precioHtg;
  export let moneda = "HTG";
  
  let precioConvertido = null;
  
  async function convertirMoneda() {
    const response = await fetch(`/api/convert?amount=${precioHtg}&from=HTG&to=${moneda}`);
    const data = await response.json();
    precioConvertido = data.converted_amount;
  }
</script>

<div>
  {#if precioConvertido}
    <p>{precioConvertido.toFixed(2)} {moneda}</p>
  {:else}
    <p>{precioHtg} HTG</p>
    <button on:click={convertirMoneda}>
      Convertir a {moneda}
    </button>
  {/if}
</div>
