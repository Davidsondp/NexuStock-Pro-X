<script>
  import { onMount } from 'svelte';
  import UserModal from './UserModal.svelte';
  
  let users = [];
  let selectedUser = null;
  let showModal = false;
  let isLoading = false;
  
  async function fetchUsers() {
    isLoading = true;
    try {
      const response = await fetch('/api/v1/users');
      users = await response.json();
    } finally {
      isLoading = false;
    }
  }
  
  function openEditModal(user) {
    selectedUser = user;
    showModal = true;
  }
  
  async function handleDelete(userId) {
    if (!confirm('¿Estás seguro de desactivar este usuario?')) return;
    
    try {
      await fetch(`/api/v1/users/${userId}`, {
        method: 'DELETE'
      });
      await fetchUsers();
    } catch (error) {
      alert('Error al desactivar usuario');
    }
  }
  
  onMount(fetchUsers);
</script>

<div class="space-y-4">
  <div class="flex justify-between items-center">
    <h1 class="text-2xl font-bold">Gestión de Usuarios</h1>
    <button 
      on:click={() => openEditModal(null)}
      class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
    >
      Nuevo Usuario
    </button>
  </div>
  
  {#if isLoading}
    <div class="text-center py-8">Cargando usuarios...</div>
  {:else}
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nombre</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Rol</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each users as user}
            <tr class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{user.full_name || '-'}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {user.email}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  user.role === 'admin' ? 'bg-purple-100 text-purple-800' :
                  user.role === 'manager' ? 'bg-blue-100 text-blue-800' :
                  'bg-green-100 text-green-800'
                }">
                  {user.role}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  user.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }">
                  {user.is_active ? 'Activo' : 'Inactivo'}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button 
                  on:click={() => openEditModal(user)}
                  class="text-blue-600 hover:text-blue-900 mr-3"
                >
                  Editar
                </button>
                {#if user.is_active}
                  <button 
                    on:click={() => handleDelete(user.id)}
                    class="text-red-600 hover:text-red-900"
                  >
                    Desactivar
                  </button>
                {/if}
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  {/if}
  
  {#if showModal}
    <UserModal 
      user={selectedUser} 
      onClose={() => {
        showModal = false;
        selectedUser = null;
      }}
      onSave={fetchUsers}
    />
  {/if}
</div>
