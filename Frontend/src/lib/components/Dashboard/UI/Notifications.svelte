<script>
  import { InlineNotification } from "carbon-components-svelte";
  export let success = false;
  export let error = false;
</script>

{#if success}
  <InlineNotification
    kind="success"
    title="Success"
    subtitle="Optimization successful! Redirecting..."
    timeout="3000"
  />
{/if}

{#if error}
  <InlineNotification
    kind="error"
    title="Error"
    subtitle="There was a problem submitting the optimization data."
    timeout="5000"
  />
{/if}
