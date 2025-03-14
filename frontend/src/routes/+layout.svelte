<script>
  import '../app.css';
  import { page } from '$app/stores';
</script>

<div class="min-h-screen flex flex-col">
  <header class="bg-primary-700 text-white shadow-md">
    <div class="container mx-auto px-4 py-4 flex justify-between items-center">
      <a href="/" class="text-2xl font-bold">Budgey</a>
      <nav>
        <ul class="flex space-x-6">
          <li><a href="/" class="hover:text-primary-200 {$page.url.pathname === '/' ? 'text-primary-200' : ''}">Dashboard</a></li>
          <li><a href="/budgets" class="hover:text-primary-200 {$page.url.pathname.startsWith('/budgets') ? 'text-primary-200' : ''}">Budgets</a></li>
          <li><a href="/transactions" class="hover:text-primary-200 {$page.url.pathname.startsWith('/transactions') ? 'text-primary-200' : ''}">Transactions</a></li>
          <li><a href="/analysis" class="hover:text-primary-200 {$page.url.pathname.startsWith('/analysis') ? 'text-primary-200' : ''}">Analysis</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main class="flex-grow container mx-auto px-4 py-8">
    <slot />
  </main>

  <footer class="bg-gray-100 border-t border-gray-200">
    <div class="container mx-auto px-4 py-6 text-center text-gray-600">
      <p>© {new Date().getFullYear()} Budgey - YNAB Data Sync and Budget Analysis Platform</p>
    </div>
  </footer>
</div>