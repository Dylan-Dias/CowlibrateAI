<script>
  import {
    Header,
    HeaderNav,
    HeaderNavItem
  } from "carbon-components-svelte";

  import { goto } from "$app/navigation";

  // ------------------------
  // Props
  // ------------------------
  export let onLogout; // <-- Add this line
  export let onNavigate; // If you want to use the onNavigate prop too

  function navigateTo(path) {
    if (onNavigate) onNavigate(path);
    else goto(path);
  }
</script>

<Header company="Dairy Dashboard" platformName="Milk Yield">
  <HeaderNav>
    <HeaderNavItem on:click={() => navigateTo("/analytics")}> Bovine Analytics </HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>
