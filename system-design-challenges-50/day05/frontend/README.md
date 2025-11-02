# Requirements Tracker Frontend

This is the frontend application for the Scalable Requirements Tracker built with Vue 3, Vite, and Tailwind CSS.

## Features

- User authentication (login/register)
- Dashboard with project overview
- Requirements management (create, read, update, delete)
- Version tracking for requirements
- Project management

## Tech Stack

- Vue 3 (Composition API)
- Vite (Build tool)
- Vue Router (Navigation)
- Pinia (State management)
- Tailwind CSS (Styling)
- Axios (HTTP client)

## Getting Started

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Preview the production build:
   ```bash
   npm run preview
   ```

## Project Structure

```
src/
├── api/          # API clients
├── assets/       # Images and static assets
├── components/   # Reusable Vue components
├── router/       # Vue Router configuration
├── store/        # Pinia stores
├── styles/       # CSS styles
├── views/        # Page components
├── App.vue       # Root component
└── main.js       # Application entry point
```

## Configuration

The application can be configured using environment variables:

- `VITE_API_BASE_URL` - Base URL for the backend API (default: http://localhost:8000/api/v1)

## Development

### Linting

```bash
npm run lint
```

### Testing

```bash
npm run test
```