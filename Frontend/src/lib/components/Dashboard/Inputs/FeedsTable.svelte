<script>
  import { NumberInput, TextInput, Button } from "carbon-components-svelte";
  import { onMount } from "svelte";

  export let feeds = [];
  export let onAddFeed = () => {};

  // Auto-create one feed row if none exist
  onMount(() => {
    if (feeds.length === 0) {
      onAddFeed();
    }
  });
</script>

<h2>Feeds</h2>

{#each feeds as f (f.id)}
  <div class="grid-row">
    <TextInput 
      labelText="Feed Type" 
      placeholder="e.g. Hay"
      bind:value={f.feed_type} 
    />

    <NumberInput 
      label="Feed Quantity" 
      min="0" 
      bind:value={f.feed_quantity} 
    />

    <NumberInput 
      label="Feed Percentage" 
      min="0" 
      bind:value={f.feed_percentage} 
    />
  </div>
{/each}

<Button kind="ghost" on:click={onAddFeed}>+ Add Feed</Button>

