<script>
  import { onMount } from 'svelte';
  export let product;
  export let onSave;
  export let onClose;

  let editedProduct = {};
  let isLoading = false;

  $: if (product) {
    editedProduct = {
      name: {...product.name},
      price_htg: product.price_htg,
      stock: product.stock
    };
  }

  async function handleSave() {
    isLoading = true;
    try {
      await onSave(editedProduct);
      onClose();
    } catch (error) {
      alert("Error al guardar: " + error.message);
    } finally {
      isLoading = false;
    }
  }
</script>

{#if product}
<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
    <div class="p-6">
      <h2 class="text-xl font-bold mb-4">Editar Producto</h2>
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre (ES)</label>
          <input
            bind:value={editedProduct.name.es}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Precio (HTG)</label>
          <input
            type="number"
            bind:value={editedProduct.price_htg}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Stock</label>
          <input
            type="number"
            bind:value={editedProduct.stock}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>

      <div class="mt-6 flex justify-end space-x-3">
        <button
          on:click={onClose}
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Cancelar
        </button>
        <button
          on:click={handleSave}
          disabled={isLoading}
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
        >
          {isLoading ? 'Guardando...' : 'Guardar'}
        </button>
      </div>
    </div>
  </div>
</div>
{/if}
