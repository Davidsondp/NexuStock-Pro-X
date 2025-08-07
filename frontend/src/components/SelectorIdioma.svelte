<script>
  const idiomas = [
    { codigo: "es", nombre: "Español" },
    { codigo: "ht", nombre: "Creole Haitiano" },
    { codigo: "en", nombre: "Inglés" },
    { codigo: "fr", nombre: "Francés" }
  ];

  function cambiarIdioma(codigo) {
    fetch("/api/config/idioma", {
      method: "POST",
      body: JSON.stringify({ idioma: codigo })
    });
    location.reload();
  }
</script>

<select on:change={(e) => cambiarIdioma(e.target.value)}>
  {#each idiomas as idioma}
    <option value={idioma.codigo}>{idioma.nombre}</option>
  {/each}
</select>
