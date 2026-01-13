<script>
  import { Button, InlineLoading } from 'carbon-components-svelte';

  export let loading = false;
  export let text = 'Submit';
  export let kind = 'primary';
  export let size = 'small';
</script>

<Button
  type="submit"
  {kind}
  {size}
  disabled={loading}
>
  {#if loading}
    <InlineLoading description="Processing..." />
  {:else}
    {text}
  {/if}
</Button>
