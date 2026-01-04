<script>
  import { Modal } from "carbon-components-svelte";

  export let open = false;
</script>

<Modal
  bind:open
  modalHeading="Welcome!"
  primaryButtonText="Got it"
  secondaryButtonText="Close"
  on:requestClose={() => (open = false)}
  on:requestSubmit={() => (open = false)}
>
  <p>
    Thanks for registering! Before you begin, please review this information.
  </p>
</Modal>
