<script>
  import { onMount } from 'svelte';
  let email = '';
  let password = '';
  let emailError = '';
  let passwordError = '';
  let isLoading = false;

  function validateEmail() {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email) {
      emailError = 'El correo es requerido';
    } else if (!re.test(email)) {
      emailError = 'Correo electrónico inválido';
    } else {
      emailError = '';
    }
  }

  function validatePassword() {
    if (!password) {
      passwordError = 'La contraseña es requerida';
    } else if (password.length < 6) {
      passwordError = 'Mínimo 6 caracteres';
    } else {
      passwordError = '';
    }
  }

  async function handleSubmit() {
    validateEmail();
    validatePassword();
    
    if (emailError || passwordError) return;

    isLoading = true;
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
      
      if (!response.ok) {
        throw new Error('Credenciales inválidas');
      }
      
      // Redirección después de login exitoso
      window.location.href = '/dashboard';
    } catch (error) {
      alert(error.message);
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="max-w-md mx-auto mt-10">
  <form on:submit|prevent={handleSubmit} class="space-y-6">
    <div>
      <label for="email" class="block text-sm font-medium text-gray-700">Correo electrónico</label>
      <input
        type="email"
        id="email"
        bind:value={email}
        on:input={validateEmail}
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      />
      {#if emailError}
        <p class="mt-2 text-sm text-red-600">{emailError}</p>
      {/if}
    </div>

    <div>
      <label for="password" class="block text-sm font-medium text-gray-700">Contraseña</label>
      <input
        type="password"
        id="password"
        bind:value={password}
        on:input={validatePassword}
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
      />
      {#if passwordError}
        <p class="mt-2 text-sm text-red-600">{passwordError}</p>
      {/if}
    </div>

    <div>
      <button
        type="submit"
        disabled={isLoading}
        class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
      >
        {isLoading ? 'Iniciando sesión...' : 'Iniciar sesión'}
      </button>
    </div>
  </form>
</div>
