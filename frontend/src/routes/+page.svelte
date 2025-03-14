<script>
  import { onMount } from 'svelte';
  
  let budgets = [];
  let loading = true;
  let error = null;
  
  onMount(async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/budgets');
      if (!response.ok) {
        throw new Error(`Error fetching budgets: ${response.statusText}`);
      }
      const data = await response.json();
      budgets = data.budgets;
    } catch (err) {
      error = err.message;
      console.error('Failed to fetch budgets:', err);
    } finally {
      loading = false;
    }
  });
</script>

<div class="space-y-8">
  <div class="flex justify-between items-center">
    <h1 class="text-3xl font-bold">Dashboard</h1>
    <div class="text-sm text-gray-500">
      Last updated: {new Date().toLocaleString()}
    </div>
  </div>
  
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4">Welcome to Budgey</h2>
    <p class="text-gray-700">
      Budgey is your YNAB data sync and budget analysis platform. View your budgets, track your spending,
      and get insights into your financial health.
    </p>
  </div>
  
  <div class="bg-white rounded-lg shadow-md p-6">
    <h2 class="text-xl font-semibold mb-4">Your Budgets</h2>
    
    {#if loading}
      <div class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    {:else if error}
      <div class="bg-red-50 text-red-700 p-4 rounded-md">
        {error}
      </div>
    {:else if budgets.length === 0}
      <div class="text-center py-8 text-gray-500">
        <p>No budgets found. Please check your YNAB connection.</p>
      </div>
    {:else}
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {#each budgets as budget}
          <a href="/budgets/{budget.id}" class="block bg-gray-50 hover:bg-gray-100 p-4 rounded-md border border-gray-200 transition">
            <h3 class="font-medium text-lg">{budget.name}</h3>
            <p class="text-sm text-gray-500">Last modified: {new Date(budget.last_modified_on).toLocaleDateString()}</p>
          </a>
        {/each}
      </div>
    {/if}
  </div>
</div>