<script>
  import { NumberInput, TextInput, Button } from "carbon-components-svelte";
  import { onMount } from "svelte";

  export let bovines = [];
  export let onAddBovine = () => {};

  // Auto create one bovine row if none exist
  onMount(() => {
    if (bovines.length === 0) {
      onAddBovine();
    }
  });
</script>

<h2>Bovines</h2>

{#each bovines as b (b.id)}
  <div class="grid-row">
    <TextInput label="Milk Yield" placeholder="Milk Yield" bind:value={b.milk_yield} />
    <TextInput labelText="Health" placeholder="Health Status" bind:value={b.health} />
    <TextInput labelText="Breed" placeholder="e.g. Holstein" bind:value={b.breed} />
  </div>
  <div class="grid-row">
    <TextInput labelText="Lactation Stage" placeholder="Stage" bind:value={b.lactation_stage} />
    <TextInput label="Age" placeholder="Age" bind:value={b.age} />
  </div>
{/each}

<Button kind="ghost" on:click={onAddBovine}>+ Add Bovine</Button>

