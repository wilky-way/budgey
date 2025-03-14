# Budgey Frontend

The Frontend is a modern web application that provides a user interface for interacting with the Budgey platform. It displays YNAB data and budget analysis in an intuitive and responsive interface.

## Architecture

The Frontend is built with Svelte 5, a radical new approach to building user interfaces. It uses a component-based architecture with the following key technologies:

- **Svelte 5**: Modern UI framework with fine-grained reactivity
- **SvelteKit**: Application framework with routing and SSR
- **Tailwind CSS 4**: Utility-first CSS framework
- **Chart.js**: Data visualization library

## Key Features

- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Dashboards**: Visual representation of budget data
- **Real-time Updates**: Reactive UI that updates as data changes
- **Accessibility**: WCAG-compliant interface
- **Dark Mode**: Support for light and dark themes (to be implemented)

## Directory Structure

```
frontend/
├── Dockerfile          # Container definition
├── package.json        # Node.js dependencies
├── svelte.config.js    # Svelte configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
├── src/
│   ├── app.html        # HTML template
│   ├── app.css         # Global styles
│   ├── lib/            # Shared components and utilities
│   ├── routes/         # Page routes
│   │   ├── +layout.svelte  # Main layout
│   │   ├── +page.svelte    # Home page
│   │   └── ...
│   ├── components/     # Reusable UI components
│   └── stores/         # Svelte stores for state management
└── tests/              # Unit and integration tests
```

## Pages

The frontend includes the following main pages:

- **Dashboard**: Overview of budget health and key metrics
- **Budgets**: List of budgets and budget details
- **Transactions**: Transaction history and management
- **Analysis**: Budget analysis and insights (Phase 2)

## Configuration

The frontend is configured using environment variables:

- `VITE_API_URL`: Backend API URL

## Running the Service

### Using Docker

```bash
docker-compose up frontend
```

### Standalone

```bash
cd frontend
npm install
npm run dev
```

The application will be available at `http://localhost:3000`.

## Development

To add new features or modify the frontend:

1. Create or update components in `src/components/`
2. Create or update pages in `src/routes/`
3. Add any shared functionality in `src/lib/`
4. Update styles in `src/app.css` or component-specific styles
5. Write tests in the `tests/` directory

## Building for Production

```bash
npm run build
```

This will create a production-ready build in the `build` directory.

## Phase 2: RAG Integration

In Phase 2, the frontend will be enhanced with:

- Natural language query interface for budget questions
- AI-powered insights and recommendations
- Visualization of spending patterns and trends
- Goal tracking and progress monitoring