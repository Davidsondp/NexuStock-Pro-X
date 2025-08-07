<script>
  import { onMount } from 'svelte';
  
  let products = [];
  
  onMount(async () => {
    const response = await fetch('/api/v1/products?low_stock=true');
    products = await response.json();
  });
</script>

<div class="overflow-x-auto">
  <table class="min-w-full divide-y divide-gray-200">
    <thead class="bg-gray-50">
      <tr>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Producto</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Actual</th>
        <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Stock Mínimo</th>
      </tr>
    </thead>
    <tbody class="bg-white divide-y divide-gray-200">
      {#each products as product}
        <tr class="hover:bg-gray-50">
          <td class="px-6 py-4 whitespace-nowrap">
            <div class="flex items-center">
              <div class="ml-4">
                <div class="text-sm font-medium text-gray-900">{product.name.es}</div>
                <div class="text-sm text-gray-500">{product.barcode}</div>
              </div>
            </div>
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-red-600 font-bold">
            {product.stock}
          </td>
          <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
            {product.stock_min}
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
