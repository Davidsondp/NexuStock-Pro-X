<script>
  let idiomas = [
    { codigo: "es", nombre: "Español" },
    { codigo: "ht", nombre: "Kreyòl Ayisyen" },
    { codigo: "en", nombre: "English" }
  ];
  
  function cambiarIdioma(codigo) {
    fetch("/api/config/idioma", {
      method: "POST",
      body: JSON.stringify({ idioma: codigo })
    });
    location.reload();  // Recargar para aplicar cambios
  }
</script>

<select on:change={(e) => cambiarIdioma(e.target.value)}>
  {#each idiomas as idioma}
    <option value={idioma.codigo}>{idioma.nombre}</option>
  {/each}
</select>
