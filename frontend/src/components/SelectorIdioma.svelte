<script>
  const idiomas = [
    { codigo: "es", nombre: "Español" },
    { codigo: "ht", nombre: "Kreyòl Ayisyen" },
    { codigo: "en", nombre: "English" },
    { codigo: "fr", nombre: "Français" },
    { codigo: "pt", nombre: "Português" },
    { codigo: "zh", nombre: "中文" },
    { codigo: "ar", nombre: "العربية" }
  ];

  function cambiarIdioma(codigo) {
    fetch("/api/config/locale", {
      method: "POST",
      body: JSON.stringify({ locale: codigo })
    });
    location.reload();
  }
</script>

<select on:change={(e) => cambiarIdioma(e.target.value)}>
  {#each idiomas as idioma}
    <option value={idioma.codigo}>{idioma.nombre}</option>
  {/each}
</select>
