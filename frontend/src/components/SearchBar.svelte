<script>
  import { debounce } from 'lodash-es';
  
  export let onSearch;
  
  let query = '';
  let category = '';
  let priceRange = [0, 10000];
  let showLowStock = false;
  
  const doSearch = debounce(() => {
    onSearch({
      query,
      category,
      minPrice: priceRange[0],
      maxPrice: priceRange[1],
      lowStock: showLowStock
    });
  }, 500);
</script>

<div class="bg-white p-4 shadow rounded-lg">
  <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
    <!-- Búsqueda por texto -->
    <div class="md:col-span-2">
      <label class="block text-sm font-medium text-gray-700">Buscar</label>
      <input
        type="text"
        bind:value={query}
        on:input={doSearch}
        placeholder="Nombre, código o descripción"
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      />
    </div>
    
    <!-- Filtro por categoría -->
    <div>
      <label class="block text-sm font-medium text-gray-700">Categoría</label>
      <select
        bind:value={category}
        on:change={doSearch}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="">Todas</option>
        <option value="electronica">Electrónica</option>
        <option value="alimentos">Alimentos</option>
        <!-- Más opciones -->
      </select>
    </div>
    
    <!-- Filtro por stock -->
    <div class="flex items-end">
      <label class="flex items-center">
        <input
          type="checkbox"
          bind:checked={showLowStock}
          on:change={doSearch}
          class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
        />
        <span class="ml-2 text-sm text-gray-700">Solo bajo stock</span>
      </label>
    </div>
  </div>
</div>
