<script>
  import { onMount } from 'svelte';
  
  let movements = [];
  let filters = {
    product: '',
    type: '',
    startDate: '',
    endDate: ''
  };
  let isLoading = false;
  
  async function fetchMovements() {
    isLoading = true;
    try {
      const params = new URLSearchParams();
      if (filters.product) params.append('product_id', filters.product);
      if (filters.type) params.append('type', filters.type);
      if (filters.startDate) params.append('start_date', filters.startDate);
      if (filters.endDate) params.append('end_date', filters.endDate);
      
      const response = await fetch(`/api/v1/movements?${params.toString()}`);
      movements = await response.json();
    } finally {
      isLoading = false;
    }
  }
  
  onMount(fetchMovements);
</script>

<div class="space-y-4">
  <!-- Filtros -->
  <div class="bg-white p-4 rounded-lg shadow grid grid-cols-1 md:grid-cols-4 gap-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">Producto</label>
      <input 
        type="text" 
        bind:value={filters.product}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      >
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Tipo</label>
      <select 
        bind:value={filters.type}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      >
        <option value="">Todos</option>
        <option value="entrada">Entradas</option>
        <option value="salida">Salidas</option>
        <option value="ajuste">Ajustes</option>
      </select>
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Desde</label>
      <input 
        type="date" 
        bind:value={filters.startDate}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      >
    </div>
    
    <div>
      <label class="block text-sm font-medium text-gray-700">Hasta</label>
      <input 
        type="date" 
        bind:value={filters.endDate}
        class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
      >
    </div>
    
    <div class="md:col-span-4 flex justify-end">
      <button 
        on:click={fetchMovements}
        disabled={isLoading}
        class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Cargando...' : 'Filtrar'}
      </button>
    </div>
  </div>
  
  <!-- Tabla de resultados -->
  <div class="bg-white shadow rounded-lg overflow-hidden">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cantidad</th>
          <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each movements as movement}
          <tr class="hover:bg-gray-50">
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {new Date(movement.created_at).toLocaleString()}
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="text-sm font-medium text-gray-900">{movement.product.name}</div>
              <div class="text-sm text-gray-500">{movement.product.barcode}</div>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
              <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                movement.type === 'entrada' ? 'bg-green-100 text-green-800' : 
                movement.type === 'salida' ? 'bg-red-100 text-red-800' : 
                'bg-yellow-100 text-yellow-800'
              }">
                {movement.type}
              </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm ${
              movement.type === 'entrada' ? 'text-green-600' : 'text-red-600'
            }">
              {movement.type === 'entrada' ? '+' : '-'}{movement.quantity}
            </td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
              {movement.user.name}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>
