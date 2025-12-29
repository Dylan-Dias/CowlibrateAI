<script>
  import { onMount } from "svelte";
  import DatabaseView from "$lib/components/DatabaseView/DatabaseView.svelte";

  let entries = [];
  let loading = true;
  let error = null;

  onMount(async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await fetch("https://cowlibrate.onrender.com/api/submissions", {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "application/json",
        }
      });

      if (!res.ok) throw new Error("Failed to load submissions.");

      entries = await res.json();
    } catch (err) {
      error = err.message;
    } finally {
      loading = false;
    }
  });
</script>

{#if loading}
  <p>Loading your submissions...</p>

{:else if error}
  <p style="color: red;">{error}</p>

{:else}
  <DatabaseView {entries} />
{/if}
