<script>
  import { onMount } from 'svelte';
  import Results from '$lib/components/Results.svelte';

  // --- State ---
  let userCows = [];   // Populated dynamically from user input
  let userFeeds = [];  // Populated dynamically from user input
  let results = [];    // Will hold optimization results
  let errorMsg = '';   // For displaying fetch or backend errors

  let currentRequest;

  // --- Trigger optimization when both cows and feeds are filled ---
  $: if (userCows.length > 0 && userFeeds.length > 0) {
    optimizeCows();
  }

  // --- Core function ---
  async function optimizeCows() {
    if (currentRequest) currentRequest.abort();
    currentRequest = new AbortController();
    const { signal } = currentRequest;

    const payload = {
      bovines: userCows,
      feeds: userFeeds
    };

    try {
      const res = await fetch('http://localhost:8080/api/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
        signal
      });

      if (!res.ok) {
        // Try to read JSON error; if not JSON, read text
        const text = await res.text();
        console.error('Server error:', text);
        errorMsg = `Backend returned error: ${res.status}`;
        results = [];
        return;
      }

      const data = await res.json();
      results = data.feed_allocation || [];
      errorMsg = '';

    } catch (err) {
      if (err.name === 'AbortError') return; // Ignore cancels
      console.error('Fetch error:', err);
      errorMsg = 'Failed to fetch optimization results.';
      results = [];
    }
  }
</script>

<!-- --- UI --- -->
{#if errorMsg}
  <div class="text-red-600 font-medium">{errorMsg}</div>
{/if}

{#if results.length > 0}
  <Results {results} />
{:else}
  <p class="text-gray-500">Awaiting optimization results...</p>
{/if}
