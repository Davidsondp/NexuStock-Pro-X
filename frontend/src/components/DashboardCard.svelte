<script>
  export let title;
  export let value;
  export let icon;
  export let alert = false;
</script>

<div class="bg-white p-4 rounded-lg shadow border-l-4 ${
  alert ? 'border-red-500' : 'border-indigo-500'
}">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-sm font-medium text-gray-500">{title}</p>
      <p class="text-2xl font-semibold">
        {value !== undefined ? value : '--'}
      </p>
    </div>
    <span class="text-3xl">{icon}</span>
  </div>
</div>
