<script>
  export let user;
  export let onClose;
  export let onSave;
  
  let formData = {
    email: '',
    full_name: '',
    password: '',
    role: 'user'
  };
  let isSubmitting = false;
  let error = '';
  
  $: if (user) {
    formData = {
      email: user.email,
      full_name: user.full_name || '',
      password: '',
      role: user.role
    };
  }
  
  async function handleSubmit() {
    isSubmitting = true;
    error = '';
    
    try {
      const url = user ? `/api/v1/users/${user.id}` : '/api/v1/users';
      const method = user ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      
      if (!response.ok) {
        throw new Error(await response.text());
      }
      
      onClose();
      onSave();
    } catch (err) {
      error = err.message;
    } finally {
      isSubmitting = false;
    }
  }
  
  $: isFormValid = formData.email && 
    (user || formData.password) && 
    formData.role;
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
    <div class="p-6">
      <h2 class="text-xl font-bold mb-4">
        {user ? 'Editar Usuario' : 'Nuevo Usuario'}
      </h2>
      
      {#if error}
        <div class="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      {/if}
      
      <div class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            bind:value={formData.email}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
            disabled={!!user}
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Nombre Completo</label>
          <input
            type="text"
            bind:value={formData.full_name}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">
            {user ? 'Nueva Contraseña (opcional)' : 'Contraseña'}
          </label>
          <input
            type="password"
            bind:value={formData.password}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
          >
        </div>
        
        <div>
          <label class="block text-sm font-medium text-gray-700">Rol</label>
          <select
            bind:value={formData.role}
            class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3"
          >
            <option value="user">Usuario</option>
            <option value="manager">Gestor</option>
            <option value="admin">Administrador</option>
          </select>
        </div>
      </div>
      
      <div class="mt-6 flex justify-end space-x-3">
        <button
          on:click={onClose}
          class="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50"
        >
          Cancelar
        </button>
        <button
          on:click={handleSubmit}
          disabled={!isFormValid || isSubmitting}
          class="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          {isSubmitting ? 'Guardando...' : 'Guardar'}
        </button>
      </div>
    </div>
  </div>
</div>
