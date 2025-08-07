<script>
  import { onMount } from 'svelte';
  
  let reportType = 'products';
  let format = 'csv';
  let filters = {
    lowStock: false,
    category: '',
    startDate: '',
    endDate: '',
    movementType: ''
  };
  
  let categories = [];
  let isLoadingCategories = false;
  
  async function fetchCategories() {
    isLoadingCategories = true;
    try {
      const response = await fetch('/api/v1/products/categories');
      categories = await response.json();
    } finally {
      isLoadingCategories = false;
    }
  }
  
  function generateReport() {
    let url = `/api/v1/reports/${reportType}/${format}?`;
    const params = new URLSearchParams();
    
    if (reportType === 'products') {
      if (filters.lowStock) params.append('low_stock', 'true');
      if (filters.category) params.append('category', filters.category);
    } else {
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      if (filters.movementType) params.append('type', filters.movementType);
    }
    
    window.open(url + params.toString(), '_blank');
  }
  
  onMount(fetchCategories);
</script>

<div class="bg-white p-6 rounded-lg shadow">
  <h2 class="text-xl font-bold mb-6">Generar Reporte</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <!-- Selección de tipo y formato -->
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Reporte</label>
        <select 
          bind:value={reportType}
          class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
        >
          <option value="products">Productos</option>
          <option value="movements">Movimientos</option>
        </select>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">Formato</label>
        <select 
          bind:value={format}
          class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
        >
          <option value="csv">CSV</option>
          <option value="excel">Excel</option>
          <option value="pdf">PDF</option>
        </select>
      </div>
    </div>
    
    <!-- Filtros específicos -->
    <div class="space-y-4">
      {#if reportType === 'products'}
        <div>
          <label class="flex items-center">
            <input 
              type="checkbox" 
              bind:checked={filters.lowStock}
              class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
            />
            <span class="ml-2 text-sm text-gray-700">Solo productos con stock bajo</span>
          </label>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Categoría</label>
          <select 
            bind:value={filters.category}
            class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
            disabled={isLoadingCategories}
          >
            <option value="">Todas las categorías</option>
            {#each categories as category}
              <option value={category}>{category}</option>
            {/each}
          </select>
        </div>
      {:else}
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Desde</label>
            <input 
              type="date" 
              bind:value={filters.startDate}
              class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Hasta</label>
            <input 
              type="date" 
              bind:value={filters.endDate}
              class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
            />
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Tipo de Movimiento</label>
          <select 
            bind:value={filters.movementType}
            class="w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
          >
            <option value="">Todos</option>
            <option value="entrada">Entradas</option>
            <option value="salida">Salidas</option>
            <option value="ajuste">Ajustes</option>
          </select>
        </div>
      {/if}
    </div>
  </div>
  
  <div class="mt-6 flex justify-end">
    <button
      on:click={generateReport}
      class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
    >
      Generar Reporte
    </button>
  </div>
</div>
