<script>
  import { Header, HeaderNav, HeaderNavItem } from "carbon-components-svelte";
  export let onNavigate = (path) => {};
  export let onGenerateReport = () => {};
  export let onLogout = () => {};
</script>

<Header company="CowlibrateAI Dashboard">
  <HeaderNav>
    <HeaderNavItem on:click={() => onNavigate('/cow')}>Bovine Entry</HeaderNavItem>
    <HeaderNavItem on:click={() => onNavigate('/dbview')}>Herd View</HeaderNavItem>
    <HeaderNavItem on:click={onGenerateReport}>Generate Report</HeaderNavItem>
    <HeaderNavItem on:click={onLogout}>Logout</HeaderNavItem>
  </HeaderNav>
</Header>

<style>
  :global(.bx--header__name) {
    color: white !important;
    font-weight: 700;
  }

  :global(.bx--header__nav-item) {
    color: white !important;
  }

  :global(.bx--header__nav-item:hover) {
    color: #4fc3f7 !important;
  }
</style>
