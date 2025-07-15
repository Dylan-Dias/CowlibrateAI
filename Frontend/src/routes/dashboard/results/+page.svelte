<script>
  import Results from '$lib/components/Results.svelte';
  import { onMount } from 'svelte';

  let selectedCows = [];

  onMount(async () => {
    const res = await fetch('http://localhost:8080/api/optimize-run/cows');
    const data = await res.json();
    selectedCows = data.selected_cows || [];
  });
</script>

<Results {selectedCows} />
