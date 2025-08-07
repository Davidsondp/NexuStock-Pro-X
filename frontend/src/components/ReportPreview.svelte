<script>
  export let data;
  export let columns;
  export let title;
  
  $: visibleData = data.slice(0, 5);
</script>

<div class="bg-white p-4 rounded-lg shadow mb-6">
  <h3 class="text-lg font-semibold mb-4">{title} (Previsualización)</h3>
  
  <div class="overflow-x-auto">
    <table class="min-w-full divide-y divide-gray-200">
      <thead class="bg-gray-50">
        <tr>
          {#each columns as col}
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              {col}
            </th>
          {/each}
        </tr>
      </thead>
      <tbody class="bg-white divide-y divide-gray-200">
        {#each visibleData as row}
          <tr class="hover:bg-gray-50">
            {#each columns as col}
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {row[col] || '-'}
              </td>
            {/each}
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
  
  <div class="mt-2 text-sm text-gray-500">
    Mostrando {visibleData.length} de {data.length} registros
  </div>
</div>
