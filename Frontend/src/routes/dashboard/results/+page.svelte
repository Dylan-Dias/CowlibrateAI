<script>
  import { onMount } from 'svelte';
  import Results from '$lib/components/Results.svelte'; 

  selectedCows = [
  { id: 1, breed: 'Holstein', milk_yield: 25, health: 'Good', lactation_stage: 'Early', age: 4 },
  { id: 2, breed: 'Jersey', milk_yield: 20, health: 'Fair', lactation_stage: 'Late', age: 5 }
];

  let userCows = [];   // Filled dynamically from user input
  let userFeeds = [];  // Filled dynamically from user input

  // Whenever userCows or userFeeds change, fetch the optimized results
  $: if (userCows.length && userFeeds.length) {
    optimizeCows();
  }

  let currentRequest;

  async function optimizeCows() {
    // Cancel previous request if still running
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
        console.error('Optimize error:', await res.json());
        return;
      }

      const data = await res.json();
      selectedCows = data.feed_allocation || [];
    } catch (err) {
      if (err.name !== 'AbortError') console.error(err);
    }
  }
</script>

<Results {selectedCows} />
